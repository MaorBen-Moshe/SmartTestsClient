import unittest
import pytest
from models.config_manager import ConfigManager


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.config = ConfigManager()
        self.config.init_configs("../config.ini")

    @pytest.fixture(autouse=True)
    def prepare_client_feature(self, client):
        self.client_feature = client
