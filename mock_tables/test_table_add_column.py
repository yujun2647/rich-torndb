from rich_torndb.init_tables import TableInit
from mock_tables.test_base import TestBase


class TestTableAddColumn(TestBase):
    """
    CREATE TABLE IF NOT EXISTS `test_table33`(
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `user_id` bigint(20) NOT NULL COMMENT 'user_id',
      `name` varchar(20) NOT NULL COMMENT 'name',
      `test_add` varchar(20) NOT NULL COMMENT 'test_add',
      PRIMARY KEY (`id`) USING BTREE,
      UNIQUE KEY `user_id` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
    """


TableInit().init_tables()
