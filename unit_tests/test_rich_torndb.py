import random
from rich_torndb.rich_torndb import BaseConn
from rich_torndb.utils.torndb import MultipleRowsError
from unit_tests.base import BaseTestCase
from dev_env import dev_config
from rich_torndb.init_tables import TableInit
from rich_torndb.utils.changes_log import find_changes


class TestBase(BaseConn):
    def __init__(self):
        super(TestBase, self).__init__(host=dev_config.MYSQL_HOST,
                                       database=dev_config.MYSQL_DATABASE,
                                       user=dev_config.MYSQL_USER,
                                       password=dev_config.MYSQL_ROOT_PASSWORD)


class TestUser(TestBase):
    """
    CREATE TABLE IF NOT EXISTS `test_user` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `user_id` bigint(20) NOT NULL COMMENT 'user_id',
      `name` varchar(20) NOT NULL COMMENT 'name',
      `age` int(10) NOT NULL COMMENT 'age',
      PRIMARY KEY (`id`) USING BTREE,
      UNIQUE KEY `user_id` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='测试表';
    """
    __TABLE_NAME__ = "test_user"
    id = "id"
    user_id = "user_id"
    name = "name"
    age = "age"

    def get_all_users(self):
        sql = f"""select * from {self.__TABLE_NAME__}"""
        rows = self.query(sql)
        return rows


def unique_user_id():
    def _get_random():
        return random.randint(1, 9999999999)

    db = TestBase()
    user_id = _get_random()
    while db.get_exist_row(table=TestUser.__TABLE_NAME__,
                           id_keys=[TestUser.user_id],
                           data={TestUser.user_id: user_id}):
        user_id = _get_random()
    return user_id


class RichTorndbTest(BaseTestCase):
    def __init__(self, methodName='runTest'):
        super(RichTorndbTest, self).__init__(methodName=methodName)
        self.test_user = TestUser()

    def setUp(self):
        TableInit().init_tables()

    @classmethod
    def produce_one_user(cls):
        return {TestUser.user_id: unique_user_id(),
                TestUser.name: "dola", TestUser.age: random.randint(1, 19)}

    def test_insert_or_update(self, datas=None, assert_insert_num=None,
                              assert_update_num=None):
        datas = [self.produce_one_user(),
                 self.produce_one_user(),
                 self.produce_one_user()] if datas is None else datas
        if assert_insert_num is None:
            assert_insert_num = len(datas)
        if assert_update_num is None:
            assert_update_num = 0

        insert_num, update_num = self.test_user.insert_or_update_datas(
            table=TestUser.__TABLE_NAME__,
            id_keys=[TestUser.user_id],
            datas=datas)
        self.assertTrue(assert_insert_num == insert_num)
        self.assertTrue(assert_update_num == update_num)
        for data in datas:
            self.assertTrue(self.test_user.get_exist_row(
                table=TestUser.__TABLE_NAME__,
                id_keys=[TestUser.user_id],
                data=data)
            )
        return datas

    def test_delete(self):
        datas = self.test_insert_or_update()
        self.test_user.delete_datas(table=TestUser.__TABLE_NAME__,
                                    id_keys=[TestUser.user_id],
                                    datas=datas)
        for data in datas:
            self.assertFalse(self.test_user.get_exist_row(
                table=TestUser.__TABLE_NAME__,
                id_keys=[TestUser.user_id],
                data=data)
            )

    def test_update(self):
        datas = self.test_insert_or_update()
        for data in datas:
            data[TestUser.name] += str(random.randint(1, 300))
        self.test_insert_or_update(datas, assert_insert_num=0,
                                   assert_update_num=3)

    def test_update_part1(self):
        datas = self.test_insert_or_update()
        for data in datas[:1]:
            data[TestUser.name] += str(random.randint(1, 300))
        self.test_insert_or_update(datas, assert_insert_num=0,
                                   assert_update_num=1)

    def test_update_part2(self):
        datas = self.test_insert_or_update()
        for data in datas[:2]:
            data[TestUser.name] += str(random.randint(1, 300))
        self.test_insert_or_update(datas, assert_insert_num=0,
                                   assert_update_num=2)

    def test_update_part3(self):
        datas = self.test_insert_or_update()
        for data in datas[1:2]:
            data[TestUser.name] += str(random.randint(1, 300))
        self.test_insert_or_update(datas, assert_insert_num=0,
                                   assert_update_num=1)

    def test_insert_update_part(self):
        datas = self.test_insert_or_update()
        for data in datas[1:2]:
            data[TestUser.name] += str(random.randint(1, 300))
        datas.append(self.produce_one_user())
        self.test_insert_or_update(datas, assert_insert_num=1,
                                   assert_update_num=1)

    def test_update_part2_error(self):
        datas = self.test_insert_or_update()
        for data in datas[:2]:
            data[TestUser.name] += str(random.randint(1, 300))
        with self.assertRaises(AssertionError):
            self.test_insert_or_update(datas, assert_insert_num=0,
                                       assert_update_num=1)

    def test_query_all(self):
        rows = self.test_user.get_all_users()
        rows2 = self.test_user.query(f"select * from "
                                     f"{self.test_user.__TABLE_NAME__}")
        for i, row in enumerate(rows):
            row2 = rows2[i]
            changes = find_changes(row, row2)
            self.assertTrue(len(changes) == 0)

    def test_get_multi_error(self):
        with self.assertRaises(MultipleRowsError):
            self.test_user.get(f"select * from {TestUser.__TABLE_NAME__} where "
                               f"{TestUser.name} = 'dola'")
