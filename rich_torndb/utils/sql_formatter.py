from typing import *
from rich_torndb.utils.sql_invalid_errors import MissingIfNoExistsSqlError
from rich_torndb.utils.sql_valid_checker import SqlValidChecker, CreateSqlValidChecker


class SqlFormatter(object):

    def __init__(self, sql):
        self.sql = sql if sql is not None else ""
        self.formatted = False

    def _ensure_formatted(self):
        if not self.formatted:
            self.format()

    def remove_extra_space(self):
        while "  " in self.sql:
            self.sql = self.sql.replace("  ", " ")
        sql_lines = self.sql.split("\n")
        for i, sql_line in enumerate(sql_lines):
            sql_lines[i] = sql_line.strip()
        self.sql = "\n".join(sql_lines)
        self.sql = self.sql.strip()
        return self.sql

    def __check_sql_valid(self):
        temp_sql = self.sql.upper()
        SqlValidChecker(temp_sql).check()

    def format(self):
        self.remove_extra_space()
        self.__check_sql_valid()
        self.formatted = True
        return self.sql


class CreateSqlFormatter(SqlFormatter):
    ADD_COLUMN_TEMPLATE = "ALTER TABLE `{table_name}` ADD COLUMN {column_sql}"
    ADD_INDEX_TEMPLATE = "ALTER TABLE `{table_name}` ADD {index_sql}"

    def __check_sql_valid(self):
        temp_sql = self.sql.upper()
        try:
            CreateSqlValidChecker(temp_sql).check()
        except MissingIfNoExistsSqlError:
            temp_sql = self.sql.upper()
            c_idx = temp_sql.index("CREATE TABLE")
            c_idx2 = c_idx + 12
            c_idx3 = c_idx2 + 1
            self.sql = f"{self.sql[:c_idx2]} IF NOT EXISTS {self.sql[c_idx3:]}"
            self.__check_sql_valid()

    def get_table_name(self):
        self._ensure_formatted()
        sql_lines = self.sql.split("\n")
        line = sql_lines[0]
        table_name = line[line.index("`") + 1: line.rindex("`")]
        return table_name

    def format(self):
        super(CreateSqlFormatter, self).format()
        self.__check_sql_valid()
        self.formatted = True
        return self.sql

    def get_add_columns_sql_dict(self) -> Dict[str, str]:
        self._ensure_formatted()
        sql_lines = self.sql.split("\n")
        columns_sql = sql_lines[1:-1]
        columns_sql = [sql for sql in columns_sql if sql.startswith("`")]
        columns_sql_dict = dict()
        table_name = self.get_table_name()
        if not table_name:
            print("debug")
        for column_sql in columns_sql:
            if column_sql.endswith(","):
                column_sql = column_sql[0:-1]
            column = column_sql.split(" ")[0].replace("`", "")
            add_column_sql = self.ADD_COLUMN_TEMPLATE.format(
                table_name=table_name, column_sql=column_sql)
            columns_sql_dict[column] = add_column_sql
        return columns_sql_dict

    def get_add_index_sql_list(self) -> List[str]:
        self._ensure_formatted()
        sql_lines = self.sql.split("\n")
        columns_sql = sql_lines[2:-1]
        indexes_sql = [sql for sql in columns_sql
                       if sql.upper().startswith("UNIQUE KEY")
                       or sql.upper().startswith("KEY")
                       or sql.upper().startswith("PRIMARY KEY")]
        add_indexes_sql = []
        table_name = self.get_table_name()
        for index_sql in indexes_sql:
            if index_sql.endswith(","):
                index_sql = index_sql[0:-1]
            add_column_sql = self.ADD_INDEX_TEMPLATE.format(
                table_name=table_name, index_sql=index_sql)
            add_indexes_sql.append(add_column_sql)
        return add_indexes_sql
