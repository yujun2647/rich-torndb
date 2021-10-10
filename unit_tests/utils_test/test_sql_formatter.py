import logging
from unit_tests.base import BaseTestCase
from rich_torndb.utils.sql_formatter import SqlFormatter, CreateSqlFormatter
from rich_torndb.utils.log_helper import log_return


class TestSqlFormatter(BaseTestCase):

    @log_return(level=logging.DEBUG, end="\n\n")
    def do_format_use_doc(self):
        sql = self._testMethodDoc
        sql = SqlFormatter(sql).format()
        return sql

    def test_remove_extra_space(self):
        """
        CREATE TABLE IF      NOT EXISTS `test_table`(
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `user_id`  bigint(20) NOT NULL COMMENT 'user_id',
          PRIMARY KEY (`id`) USING  BTREE,
          UNIQUE KEY `user_id` (`user_id`)
        ) ENGINE=InnoDB   DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
        """
        format_sql = self.do_format_use_doc()
        self.assertFalse("  " in format_sql)


class TestCreateSqlFormatter(BaseTestCase):
    @log_return(level=logging.DEBUG, end="\n\n")
    def do_format_use_doc(self):
        sql = self._testMethodDoc
        sql = CreateSqlFormatter(sql).format()
        return sql
