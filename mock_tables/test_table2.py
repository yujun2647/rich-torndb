from mock_tables.test_base import TestBase
from rich_torndb.init_tables import TableInit


class TestTable2(TestBase):
    pass


class TestTable22(TestBase):
    pass


class TestTable11(TestBase):
    """
    CREATE TABLE IF NOT EXISTS `test_table_duplicate_class`(
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `user_id` bigint(20) NOT NULL COMMENT 'user_id',
      `name` varchar(20) NOT NULL COMMENT 'name',
      PRIMARY KEY (`id`) USING BTREE,
      UNIQUE KEY `user_id` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
    """


TableInit().init_tables()
