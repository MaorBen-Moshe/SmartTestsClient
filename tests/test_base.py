import unittest
import pytest
from models.config_manager import ConfigManager
from models.group_data import GroupData
from models.service_data import ServiceData


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.config = ConfigManager()
        self.config.init_configs("../config.ini")

    @pytest.fixture(autouse=True)
    def prepare_client_fixture(self, client):
        self.client_fixture = client

    @staticmethod
    def assert_services_map_entry(entry, old_version: str, new_version: str):
        assert type(entry) is ServiceData
        assert entry.old_version == old_version
        assert entry.new_version == new_version

    @staticmethod
    def assert_group_data(group_data: GroupData, name: str, path: str, total_count: int):
        assert group_data is not None
        assert group_data.group_name == name
        assert group_data.group_path == path
        assert group_data.total_flows_count == total_count
