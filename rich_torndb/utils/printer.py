import json
import pprint
from io import StringIO

pp = pprint.PrettyPrinter(indent=4)


def pretty_print(obj):
    pp.pprint(obj)


def to_pretty_string(obj):
    string_io = StringIO()
    if isinstance(obj, str):
        # noinspection PyBroadException
        try:
            obj = json.loads(obj)
            pprint.PrettyPrinter(stream=string_io).pprint(obj)
            return string_io.getvalue()
        except ValueError:
            return obj


if __name__ == "__main__":
    test = """
        CREATE TABLE IF      NOT EXISTS `test_table2`(
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `user_id`  bigint(20) NOT NULL COMMENT 'user_id',
          PRIMARY   KEY (`id`) USING  BTREE,
                 UNIQUE KEY `user_id` (`user_id`)
        ) ENGINE=InnoDB   DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
        """
    print(to_pretty_string(test))
