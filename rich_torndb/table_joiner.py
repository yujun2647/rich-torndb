from typing import *
from tqdm import tqdm
from rich_torndb import BaseConn


class TableJoiner(object):

    @classmethod
    def join_table(cls, base_datas: List[Dict[str, Any]],
                   table: str, fields: List[str], base_join_key: str,
                   table_join_key: str, db: BaseConn,
                   extra_conditions: [List[str], None] = None,
                   left_join: bool = False, shard_size: int = 800):
        """
             只支持内连接和左连接，默认为内连接
            左连接时，不支持指定 extra_conditions
        :param base_datas: [dict(), dict(), dict()], 基本数据，最终连表后会将数据装配进每个单元中
        :param table: str， 将要连的表
        :param fields: list， 要取出并装配的数据, 如
                             ["account", "user_id as nick_user_id"]
        :param base_join_key: str, 从 base_datas 中取出，用于连表的字段，如 user_id
        :param table_join_key: str, 从 将要连的表 中取出，用于连表的字段，如 user_id
        :param extra_conditions: list, 额外的查询条件
                                格式如 ["name in ('dola', 'tom')", "age > 2"]
        :param db: torndb.Connection, 数据库连接对象
        :param left_join: bool, 是否为左连接
        :param shard_size: int 分片查询数量
        :return:
        """
        extra_conditions = extra_conditions if extra_conditions else []

        def __separate_query(join_values) -> List[Dict[str, Any]]:
            def __get_join_values_condition_sql():
                return "{} in ('{}')".format(table_join_key,
                                             "','".join(join_values))

            if isinstance(join_values[0], str):
                join_values_condition_sql = __get_join_values_condition_sql()
            else:
                join_values = [str(value) for value in join_values]
                join_values_condition_sql = __get_join_values_condition_sql()

            conditions = [join_values_condition_sql, ] + extra_conditions

            # 拼sql
            condition_sql = " AND ".join(conditions)
            sql = f"SELECT {fields_sql} FROM {table} WHERE {condition_sql}"
            # logging.info(sql)
            return db.query(sql)

        if not base_datas:
            return

        if left_join and extra_conditions:
            raise Exception("Not support extra_conditions when using left join")

        base_join_values = [base_data[base_join_key] for base_data in
                            base_datas]

        # 连表的值可能为 None， 为空应跳过
        base_join_values = list(filter(lambda value: value, base_join_values))

        # 将类似 "user_id as c2_user_id" 提取成 c2_user_id, 用于下面对查询数据的提取
        real_fields = cls._get_real_fields(fields)

        results_map = {}
        if base_join_values:
            fields_sql = ", ".join(fields + [table_join_key, ])
            results = list()
            # 分片查询, 用于提升查询效率， 如果数量大于 1，则显示进度条
            indexes = range(0, len(base_join_values), shard_size)
            if len(base_join_values) > 1:
                indexes = tqdm(indexes, desc=f"Joining table:{table}")
            for index in indexes:
                temp_join_values = base_join_values[index: index + shard_size]
                results.extend(__separate_query(temp_join_values))

            results_map = {
                result[table_join_key]: {field: result[field] for field in
                                         real_fields}
                for result in results}

        index = 0
        while index < len(base_datas):
            data = base_datas[index]
            if data[base_join_key] in results_map:
                data.update(results_map[data[base_join_key]])
            elif left_join:
                data.update({field: None for field in real_fields})
            else:
                base_datas.pop(index)
                index -= 1
            index += 1

    @classmethod
    def _merge_datas(cls, datas1, datas2, merge_key1="user_id",
                     merge_key2="user_id"):
        datas1_map = {data[merge_key1]: data for data in datas1}

        for data in datas2:
            if data[merge_key2] not in datas1_map:
                datas1.append(data)

        return datas1

    @classmethod
    def _get_real_fields(cls, fields):
        real_fields = list()
        for field in fields:
            if " as " in field:
                real_field = field.split(" as ")[1]
            elif " AS " in field:
                real_field = field.split(" AS ")[1]
            else:
                real_field = field
            real_fields.append(real_field)
        return real_fields
