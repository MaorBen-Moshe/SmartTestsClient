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

    def assert_exception(self, function, exception: type, msg_expected: str):
        try:
            function()
        except exception as ex:
            self.assertEqual(f"{ex}", msg_expected)
        except Exception as ex:
            self.fail(f"Expected {type(exception)} exception, but got: {ex}")
        else:
            self.fail("Passed even though expected to raise exception.")

    def assert_services_map_entry(self, entry, old_version: str, new_version: str):
        self.assertIsInstance(entry, ServiceData)
        self.assertEqual(entry.old_version, old_version)
        self.assertEqual(entry.new_version, new_version)

    def assert_group_data(self, group_data: GroupData, name: str, path: str, total_count: int):
        self.assertIsNotNone(group_data)
        self.assertEqual(group_data.group_name, name)
        self.assertEqual(group_data.group_path, path)
        self.assertEqual(group_data.total_flows_count, total_count)
