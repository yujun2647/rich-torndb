from rich_torndb import BaseConn
from dev_env import dev_config
from rich_torndb.init_tables import TableInit


class TestBase(BaseConn):
    def __init__(self):
        super(TestBase, self).__init__(host=dev_config.MYSQL_HOST,
                                       database=dev_config.MYSQL_DATABASE,
                                       user=dev_config.MYSQL_USER,
                                       password=dev_config.MYSQL_ROOT_PASSWORD)


class TestTable1(TestBase):
    pass


class TestTable11(TestBase):
    """
    CREATE TABLE IF NOT EXISTS `test_table`(
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `user_id` bigint(20) NOT NULL COMMENT 'user_id',
      PRIMARY KEY (`id`) USING BTREE,
      UNIQUE KEY `user_id` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
    """


TableInit().init_tables()
