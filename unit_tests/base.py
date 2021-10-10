import os
import logging
import unittest
from rich_torndb.utils.log_helper import set_scripts_logging

set_scripts_logging(__file__, level=logging.DEBUG)


class BaseTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(BaseTestCase, self).__init__(methodName=methodName)

    def assertFileExist(self, filepath):
        self.assertTrue(os.path.exists(filepath),
                        msg=f"file not exist: {filepath}")

    def assertFileNotExist(self, filepath):
        self.assertFalse(os.path.exists(filepath),
                         msg=f"file not exist: {filepath}")

    def assertFileMtimeEqual(self, filepath1, filepath2):
        self.assertTrue(
            os.path.getmtime(filepath1) == os.path.getmtime(filepath2))

    def assertFileMtimeLater(self, filepath1, filepath2):
        self.assertTrue(
            os.path.getmtime(filepath1) > os.path.getmtime(filepath2))

    def assertFileMtimeEarlier(self, filepath1, filepath2):
        self.assertTrue(
            os.path.getmtime(filepath1) < os.path.getmtime(filepath2))
