import unittest

from models.config_manager import ConfigManager


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.config = ConfigManager()
        self.config.init_configs("../config.ini")
