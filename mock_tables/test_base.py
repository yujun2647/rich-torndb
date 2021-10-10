from dev_env import dev_config
from rich_torndb.rich_torndb import BaseConn


class TestBase(BaseConn):
    def __init__(self):
        super(TestBase, self).__init__(host=dev_config.MYSQL_HOST,
                                       database=dev_config.MYSQL_DATABASE,
                                       user=dev_config.MYSQL_USER,
                                       password=dev_config.MYSQL_ROOT_PASSWORD)
