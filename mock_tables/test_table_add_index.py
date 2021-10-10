from rich_torndb.init_tables import TableInit
from mock_tables.test_base import TestBase


class TestTable(TestBase):
    """
    CREATE TABLE IF NOT EXISTS `test_table33`(
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `user_id` bigint(20) NOT NULL COMMENT 'user_id',
      `name` varchar(20) NOT NULL COMMENT 'name',
      PRIMARY KEY (`id`) USING BTREE,
      UNIQUE KEY `user_id` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
    """


class TestTableAddIndex(TestBase):
    """
    CREATE TABLE IF NOT EXISTS `test_table33`(
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `user_id` bigint(20) NOT NULL COMMENT 'user_id',
      `name` varchar(20) NOT NULL COMMENT 'name',
      `age` int(20) NOT NULL COMMENT '年龄',
      PRIMARY KEY (`id`) USING BTREE,
      UNIQUE KEY `user_id` (`user_id`),
      KEY `name` (`name`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
    """


TableInit().init_tables()
