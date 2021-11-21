from rich_torndb.utils.sql_invalid_errors import *


class SqlValidChecker(object):
    def empty_check(self):
        if not self.sql_lines:
            raise EmptySqlError
        if len(self.sql_lines) < 3:
            raise SqlIsTooShortError

    def __init__(self, sql):
        self.sql = sql if sql else ""
        self.sql_lines = self.sql.split("\n")
        self.sql_lines = [d.strip() for d in self.sql_lines if d and d.strip()]
        self.empty_check()

    def check(self):
        pass


ALLOWED_INDEX_STARTSWITH = ["PRIMARY KEY", "UNIQUE KEY", "KEY"]
ALLOWED_COLUMN_STARTSWITH = ["`", ]


class CreateSqlValidChecker(SqlValidChecker):
    def create_sql_check(self):
        if "CREATE TABLE" not in self.sql:
            raise MissingCreateTableSqlError

    def create_table_check(self):
        self.create_sql_check()
        if "IF NOT EXISTS" not in self.sql:
            raise MissingIfNoExistsSqlError

        def _check_parse_table_name():
            line = self.sql_lines[0]
            table_name = line.split(" ")[-1].replace("`", "")
            table_name = table_name[:-1]

        _check_parse_table_name()

    def body_parentheses_check(self):
        if not self.sql_lines[0].endswith("("):
            raise StartBodyParenthesesSqlError(self.sql_lines[0])
        if not self.sql_lines[-1].startswith(")"):
            raise EndBodyParenthesesSqlError(self.sql_lines[-1],
                                             len(self.sql_lines) - 1)

    def column_invalid_startswith_check(self):
        def _check_complete(_column_sql):
            _column = _column_sql.split(" ")[0]
            return _column.endswith("`")

        for column_sql in self.sql_lines[1:-1]:
            index = self.sql_lines.index(column_sql)
            column_valid = False
            if column_sql.startswith("`") and _check_complete(column_sql):
                column_valid = True
            for allow_start in ALLOWED_INDEX_STARTSWITH:
                if column_sql.startswith(allow_start):
                    column_valid = True
            if not column_valid:
                raise ColumnInvalidSqlError(column_sql, index)

    def check(self):
        self.create_table_check()
        self.body_parentheses_check()
        self.column_invalid_startswith_check()
