from typing import *
from pymysql import ProgrammingError


class SqlSyntaxError(ProgrammingError):
    def __init__(self, error_msg: str, line: int):
        super(SqlSyntaxError, self).__init__(f"Syntax Error: \n {error_msg}"
                                             f" at line {line}")


class EmptySqlError(SqlSyntaxError):
    def __init__(self):
        super().__init__("No SQL detected", 1)


class SqlIsTooShortError(SqlSyntaxError):
    def __init__(self):
        super().__init__("SQL seems to short, at least 3 lines ?", 1)


class MissingCreateTableSqlError(SqlSyntaxError):
    def __init__(self):
        super().__init__("Missing 'CREATE TABLE'", 1)


class MissingIfNoExistsSqlError(SqlSyntaxError):
    def __init__(self):
        super().__init__("Missing 'If No Exists'", 1)


class StartBodyParenthesesSqlError(SqlSyntaxError):
    def __init__(self, line_detail):
        super().__init__(f"Body parentheses '(' should put in end of line 1, "
                         f"\nplease adjust to '{line_detail}(' ", 1)


class EndBodyParenthesesSqlError(SqlSyntaxError):
    def __init__(self, line_detail, line):
        super().__init__(
            f"Body parentheses ')' should put in front of end line,"
            f"\nplease adjust to '({line_detail}'", line)


class ColumnInvalidSqlError(SqlSyntaxError):
    def __init__(self, column_detail, line):
        super().__init__(f"Wrong Column: {column_detail} \n"
                         f"Note: Column should starts with '`' "
                         f"or 'PRIMARY KEY' or 'UNIQUE KEY'", line)


class ClassSqlCommentError(ProgrammingError):
    def __init__(self, cls: ClassVar, exp: Exception):
        class_name = f"{cls.__module__}.{cls.__name__}"
        super().__init__(f"Class sql comment error {class_name} | {exp}")
        

class ClassSqlExecuteError(ProgrammingError):
    def __init__(self, cls: ClassVar, exp: Exception):
        class_name = f"{cls.__module__}.{cls.__name__}"
        super().__init__(f"Class sql execute error, "
                         f"class_name: {class_name} | {exp}")
