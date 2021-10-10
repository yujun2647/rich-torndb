from typing import *
import logging as logger
from tqdm import tqdm

from rich_torndb.utils.changes_log import info_changes
from rich_torndb.utils.torndb import Connection, Row


def gen_condition_sql_n_vals(keys, data, is_update=False):
    conditions, values = [], []
    for key in keys:
        value = data[key]
        if value is None:
            conditions.append(
                f"{key} {'is null' if not is_update else '= NULL'}")
        else:
            conditions.append("{} = %s".format(key))
            values.append(value)
    condition_sql = (" AND ".join(conditions)
                     if not is_update else ", ".join(conditions))
    return condition_sql, values


class BaseConn(Connection):
    __TABLE_NAME__ = None

    def __init__(self, host, database, user=None, password=None,
                 max_idle_time=250, connect_timeout=10,
                 time_zone="+0:00", charset="utf8", sql_mode="TRADITIONAL"):
        """

        :rtype: object
        """
        super().__init__(host=host, database=database, user=user,
                         password=password, max_idle_time=max_idle_time,
                         connect_timeout=connect_timeout,
                         time_zone=time_zone, charset=charset,
                         sql_mode=sql_mode)

    def get_exist_row(self, table: str, id_keys: List[str],
                      data: Dict[str, Any]) -> Row:
        condition_sql, id_key_values = gen_condition_sql_n_vals(id_keys, data)
        check_exist_sql = f"SELECT id FROM {table} WHERE {condition_sql}"
        exist_row = self.get(check_exist_sql, *id_key_values)
        return exist_row

    @classmethod
    def _gen_exec_sql_and_values(cls, table: str, exist: Row,
                                 data: Dict) -> Tuple[str, List[str]]:
        keys = list(data.keys())
        if exist:
            if "id" in keys:
                keys.remove("id")
            condition_sql, values = gen_condition_sql_n_vals(keys, data,
                                                             is_update=True)
            update_sql = f"UPDATE {table} SET {condition_sql} WHERE id = %s"
            return update_sql, values + [exist["id"], ]
        else:
            keys = list(data.keys())
            values = [data[key] for key in keys]
            fields_sql = "`{}`".format("`, `".join(keys))
            values_sql = ", ".join(["%s" for _ in keys])
            insert_sql = (f"INSERT INTO {table} ({fields_sql}) "
                          f"VALUES ({values_sql})")
            return insert_sql, values

    @classmethod
    def _gen_delete_sql_and_values(cls, table: str, exist_row: Row,
                                   data: Dict) -> Tuple[str, List[str]]:
        if not exist_row:
            raise Exception("Exist row is None")
        keys = list(data.keys())
        if "id" in keys:
            keys.remove("id")
        condition_sql, values = gen_condition_sql_n_vals(keys, data)
        update_sql = f"DELETE FROM {table} WHERE id = %s"
        return update_sql, values + [exist_row["id"], ]

    def insert_or_update_datas(self, id_keys: List[str],
                               datas: List[Dict[str, Any]],
                               table: str = None):
        """
        :param id_keys: the column keys that make record unique.
                        such as ["id"] or ["day", "user_id"]
                        this method will use {id_keys} call check_exist,
                        it will raise Exception("Multiple rows") if check_exist
                        returns multiple record
        :param datas: format [dict(), dict()],
                    NOTE：the datas inside，must contains columns specified in
                    id_keys, such as
                    [
                        {"user_id" : 1324, "gender" : "0", .....}
                        {"user_id" : 1323, "gender" : "1", .....}
                        {"user_id" : 1325, "gender" : "0", .....}
                        {"user_id" : 1326, "gender" : "1", .....}
                    ]
        :param table: optional, use __TABLE_NAME__ if table is not specified
        :return:
        """
        table = self.__TABLE_NAME__ if table is None else table
        insert_num, update_num = 0, 0
        with TransactionHelper(self):
            for data in tqdm(datas, desc=f"Inserting into table:{table}"):
                try:
                    exist_row = self.get_exist_row(table, id_keys, data)
                    exec_sql, values = self._gen_exec_sql_and_values(
                        table, exist_row, data)
                    if not exist_row:
                        self.execute(exec_sql, *values)
                        insert_num += 1
                    elif info_changes(table=table,
                                      id_kvs={id_key: data[id_key]
                                              for id_key in id_keys},
                                      new_data=data, db=self):
                        self.execute(exec_sql, *values)
                        update_num += 1
                except Exception as exp:
                    warning_msg = (f"{exp}\n"
                                   f"Something happened when insert date into:"
                                   f"{table}\n"
                                   f"id_keys:{id_keys}, data:{data}")
                    logger.warning(warning_msg)
                    raise Exception(warning_msg)

        logger.info(f"Insert successfully!!! new insert num:{insert_num},"
                    f" updated num:{update_num}")
        
        return insert_num, update_num

    def delete_datas(self, id_keys: List[str],
                     datas: List[Dict[str, Any]],
                     table: str = None):
        """
        :param id_keys:
        :param datas:
        :param table:
        :return:
        """
        table = self.__TABLE_NAME__ if table is None else table
        delete_num = 0
        with TransactionHelper(self):
            for data in tqdm(datas, desc=f"Deleting from table: {table}"):
                try:
                    exist_row = self.get_exist_row(table, id_keys, data)
                    if not exist_row:
                        continue
                    delete_sql = f"DELETE FROM {table} WHERE id = %s"
                    self.execute(delete_sql, exist_row["id"])
                    delete_num += 1
                except Exception as exp:
                    warning_msg = (f"{exp}\n"
                                   f"Something happened when delete date from "
                                   f"{table}\n"
                                   f"id_keys:{id_keys}, data:{data}")
                    logger.warning(warning_msg)
                    raise Exception(warning_msg)

        logger.info(f"Delete successfully!!! delete num:{delete_num}")
        return delete_num


class TransactionHelper(object):

    def __init__(self, db):
        self.db = db

    def __enter__(self):
        self.db._ensure_connected()
        self.db._db.begin()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db._ensure_connected()
            self.db._db.rollback()
            raise exc_val
        self.db._db.commit()
