from typing import *
from rich_torndb.rich_torndb import BaseConn

from rich_torndb.utils.sql_invalid_errors import *
from rich_torndb.utils.sql_formatter import CreateSqlFormatter
from rich_torndb.utils.sql_valid_checker import CreateSqlValidChecker


class TableInit(object):
    # These are ignored errors that may happened when attempt to add column,
    # index
    IGNORE_ATTEMPT_EXECUTE_ERRORS = [
        "Duplicate column name",
        "Duplicate key name",
        "Multiple primary key defined",
    ]

    INITED_TABLE_CLASSES: Set = set()

    @classmethod
    def execute_create_sql(cls, _class: ClassVar[BaseConn], create_sql: str):
        db = _class()
        db.init_table_process = True
        _class().execute(create_sql)

    @classmethod
    def exec_add_column_sql(cls, _class: ClassVar[BaseConn],
                            add_column_sql: str):
        db = _class()
        db.init_table_process = True
        try:
            db.execute(add_column_sql)
        except Exception as exp:
            if not cls.is_ignore_error(exp):
                raise ClassSqlExecuteError(_class, exp)

    @classmethod
    def is_ignore_error(cls, exp):
        exp_str = str(exp)
        for error in cls.IGNORE_ATTEMPT_EXECUTE_ERRORS:
            if error in exp_str:
                return True
        return False

    def _do_create(self, _class: ClassVar[BaseConn],
                   sql_formatter: CreateSqlFormatter):
        try:
            create_sql = sql_formatter.format()
        except Exception as exp:
            raise ClassSqlCommentError(_class, exp)
        try:
            self.execute_create_sql(_class, create_sql)
        except Exception as exp:
            raise ClassSqlExecuteError(_class, exp)

    def _do_add_column(self, _class: ClassVar[BaseConn],
                       sql_formatter: CreateSqlFormatter):
        add_columns_sql_dict = sql_formatter.get_add_columns_sql_dict()
        successes = []
        for column, add_column_sql in add_columns_sql_dict.items():
            try:
                if successes:
                    add_column_sql += f" AFTER {successes[-1]}"
                self.exec_add_column_sql(_class, add_column_sql)
                successes.append(column)
            except ClassSqlExecuteError as exp:
                raise

    def _do_add_index(self, _class: ClassVar[BaseConn],
                      sql_formatter: CreateSqlFormatter):
        add_index_sql_list = sql_formatter.get_add_index_sql_list()
        for add_index_sql in add_index_sql_list:
            self.exec_add_column_sql(_class, add_index_sql)

    def do_init(self, _class: ClassVar[BaseConn]):
        create_sql = _class.__doc__
        if not create_sql:
            return
        sql_formatter = CreateSqlFormatter(create_sql)
        self._do_create(_class, sql_formatter)
        self._do_add_column(_class, sql_formatter)
        self._do_add_index(_class, sql_formatter)

    @classmethod
    def __is_sql_comment(cls, doc):
        try:
            CreateSqlValidChecker(doc).create_sql_check()
            return True
        except SqlSyntaxError:
            return False

    def get_sql_table_subs(self, _class: ClassVar[BaseConn]):
        subs = []
        for c in _class.__subclasses__():
            if c in self.INITED_TABLE_CLASSES:
                continue
            if self.__is_sql_comment(c.__doc__):
                subs.append(c)
            if c.__subclasses__():
                subs.extend(self.get_sql_table_subs(c))
        return subs

    def init_tables(self, base_class=BaseConn):
        init_classes = self.get_sql_table_subs(base_class)

        for init_class in init_classes:
            self.do_init(init_class)
            self.INITED_TABLE_CLASSES.add(init_class)
