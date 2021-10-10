from unit_tests.base import BaseTestCase
from rich_torndb.utils.sql_formatter import CreateSqlFormatter
from mock_tables.test_base import TestBase
from rich_torndb.init_tables import TableInit


class InitTablesTests(BaseTestCase):
    def __init__(self, methodName='runTest'):
        super(InitTablesTests, self).__init__(methodName=methodName)
        self.test_db = TestBase()

    @classmethod
    def _get_table_name(cls, _class):
        create_sql = _class.__doc__
        return CreateSqlFormatter(create_sql).get_table_name()

    def test_init_table(self):
        self.assertTrue(True)

    def get_field_schema_data(self, table_name, field_name):
        rows = self.test_db.query(f"desc {table_name}")
        field = [row for row in rows if row["Field"] == field_name][0]
        return field

    def test_add_column(self):
        from mock_tables.test_table_add_column import TestTableAddColumn
        table_name = self._get_table_name(TestTableAddColumn)
        rows = self.test_db.query(f"desc {table_name}")
        fields = {row["Field"] for row in rows}
        self.assertTrue("test_add" in fields)
        self.test_db.execute(f"ALTER TABLE {table_name} DROP COLUMN test_add ")

    def test_add_index(self):
        from mock_tables.test_table_add_index import TestTableAddIndex
        table_name = self._get_table_name(TestTableAddIndex)
        index_field = self.get_field_schema_data(table_name, "name")
        self.assertTrue(index_field["Key"] == "MUL")
        self.test_db.execute(f"DROP INDEX name ON {table_name}")
        sql_formatter = CreateSqlFormatter(TestTableAddIndex.__doc__)
        index_field = self.get_field_schema_data(table_name, "name")
        self.assertTrue(index_field["Key"] == "")
        TableInit()._do_add_index(TestTableAddIndex, sql_formatter)
        index_field = self.get_field_schema_data(table_name, "name")
        self.assertTrue(index_field["Key"] == "MUL")
