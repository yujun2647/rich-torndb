import logging

from rich_torndb.utils.sql_invalid_errors import *
from unit_tests.utils_test.test_sql_formatter import TestSqlFormatter
from rich_torndb.utils.log_helper import log_return
from rich_torndb.utils.sql_formatter import CreateSqlFormatter, SqlFormatter


class TestSqlInvalid(TestSqlFormatter):
    @log_return(level=logging.DEBUG, end="\n\n")
    def do_format_use_doc(self):
        sql = self._testMethodDoc
        sql = SqlFormatter(sql).format()
        return sql

    def test_sql_empty(self):
        with self.assertRaises(EmptySqlError):
            self.do_format_use_doc()


class TestCreateSqlInvalid(TestSqlFormatter):

    @log_return(level=logging.DEBUG, end="\n\n")
    def do_format_use_doc(self):
        sql = self._testMethodDoc
        sql = CreateSqlFormatter(sql).format()
        return sql

    def test_create_sql_too_short(self):
        """
        CREATE TABLE `test_table`(
        ) ENGINE=InnoDB   DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
        """
        with self.assertRaises(SqlIsTooShortError):
            self.do_format_use_doc()

    def test_invalid_missing_create_table(self):
        """
        IF      NOT EXISTS `test_table`(
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `user_id`  bigint(20) NOT NULL COMMENT 'user_id',
          PRIMARY   KEY (`id`) USING  BTREE,
                 UNIQUE KEY `user_id` (`user_id`)
        ) ENGINE=InnoDB   DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
        """
        with self.assertRaises(MissingCreateTableSqlError):
            self.do_format_use_doc()

    def test_invalid_missing_if_not_exists_allow(self):
        """
        CREATE TABLE `test_table`(
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `user_id`  bigint(20) NOT NULL COMMENT 'user_id',
          PRIMARY   KEY (`id`) USING  BTREE,
                 UNIQUE KEY `user_id` (`user_id`)
        ) ENGINE=InnoDB   DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
        """
        self.do_format_use_doc()

    def test_wrong_position_start_body_parentheses(self):
        """
        CREATE TABLE `test_table`
        (
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `user_id`  bigint(20) NOT NULL COMMENT 'user_id',
          PRIMARY   KEY (`id`) USING  BTREE,
                 UNIQUE KEY `user_id` (`user_id`)
        ) ENGINE=InnoDB   DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
        """
        with self.assertRaises(StartBodyParenthesesSqlError):
            self.do_format_use_doc()

    def test_wrong_position_start_body_parentheses2(self):
        """
        CREATE TABLE `test_table`
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `user_id`  bigint(20) NOT NULL COMMENT 'user_id',
          PRIMARY   KEY (`id`) USING  BTREE,
                 UNIQUE KEY `user_id` (`user_id`)
        ) ENGINE=InnoDB   DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
        """

        with self.assertRaises(StartBodyParenthesesSqlError):
            self.do_format_use_doc()

    def test_wrong_position_start_body_parentheses3(self):
        """
        CREATE TABLE `test_table`(
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `user_id`  bigint(20) NOT NULL COMMENT 'user_id',
          PRIMARY   KEY (`id`) USING  BTREE,
                 UNIQUE KEY `user_id` (`user_id`)
        ENGINE=InnoDB   DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
        """

        with self.assertRaises(EndBodyParenthesesSqlError):
            self.do_format_use_doc()

    def test_wrong_position_start_body_parentheses4(self):
        """
        CREATE TABLE `test_table`(
          `id` bigint(20) NOT NULL AUTO_INCREMENT,
          `user_id`  bigint(20) NOT NULL COMMENT 'user_id',
          PRIMARY   KEY (`id`) USING  BTREE,
                 UNIQUE KEY `user_id` (`user_id`)
        )
        ENGINE=InnoDB   DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
        """

        with self.assertRaises(EndBodyParenthesesSqlError):
            self.do_format_use_doc()

    def test_columns_invalid_startswith(self):
        """
        CREATE TABLE `test_table`(
        (  `id` bigint(20) NOT NULL AUTO_INCREMENT,
         `user_id`  bigint(20) NOT NULL COMMENT 'user_id',
          PRIMARY   KEY (`id`) USING  BTREE,
                 UNIQUE KEY `user_id` (`user_id`)
        )ENGINE=InnoDB   DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
        """

        with self.assertRaises(ColumnInvalidSqlError):
            self.do_format_use_doc()
