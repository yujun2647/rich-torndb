from rich_torndb.init_tables import TableInit
from mock_tables.test_base import TestBase


class TestTableAddColumnAfter(TestBase):
    """
    CREATE TABLE IF NOT EXISTS `test_table_add_column_after`(
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `user_id` bigint(20) NOT NULL COMMENT 'user_id',
      `test_add_after_user_id` varchar(20) NOT NULL COMMENT 'test_add',
      `name` varchar(20) NOT NULL COMMENT 'name',
      PRIMARY KEY (`id`) USING BTREE,
      UNIQUE KEY `user_id` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
    """


TableInit().init_tables()
