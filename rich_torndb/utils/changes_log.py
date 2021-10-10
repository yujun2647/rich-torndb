from typing import *
import json
import datetime
import logging as logger


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def is_num(value):
    # noinspection PyBroadException
    try:
        float(value)
        return True
    except Exception:
        return False


def union_type(*values, **kwargs):
    def union(_value):
        if isinstance(_value, datetime.datetime):
            _value = _value.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(_value, str) and is_num(_value):
            _value = float(_value)
        if is_num(_value):
            _value = round(_value, 2)
        if kwargs.get("digit_to_int") and is_num(_value):
            _value = int(_value)
        return _value

    union_values = [union(value) for value in values]
    return union_values


def info_changes(table, id_kvs, new_data, db):
    """
        log changes
    :param table: str table name about to update
    :param id_kvs: dict 要更改的记录主键，此处兼容多个字段兼容的联合主键
                  format sample { key1:value1, key2:value2 }
    :param new_data: dict 要更改的数据
    :param db: query object
    :return: 当主键对应的用户不存在时，返回None
             当原数据和新数据没有差异时，也返回None
             当原数据和新数据存在差异时，返回差异
    """

    args = [arg for arg in new_data.keys() if arg not in id_kvs]  # 过滤掉主键
    if not args:
        return None

    values = []
    id_fields = []
    for id_key, value in id_kvs.items():
        id_fields.append("{}=%s".format(id_key))
        values.append(value)

    select_sql = "SELECT {} FROM {} WHERE {}".format(", ".join(args), table,
                                                     " AND ".join(id_fields))

    old_data = db.get(select_sql, *values)
    if not old_data:
        return None

    changes = find_changes(old_data, new_data)
    if changes:
        details = json.dumps(changes, ensure_ascii=False, cls=DateEncoder)
        logger.info(f"[Record changes] table:{table}; primary:{id_kvs}; "
                    f"details:{details};")
        return changes

    return None


def find_changes(data1: Dict[str, Any], data2: Dict[str, Any],
                 data1_key="old", data2_key="new", digit_to_int=False):
    changes = dict()
    for arg, value in data1.items():
        value1, value2 = union_type(value, data2[arg],
                                    digit_to_int=digit_to_int)
        if value1 != value2:
            changes[arg] = {data1_key: value1, data2_key: value2}
    return changes
