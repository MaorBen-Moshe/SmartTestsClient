import json
import unittest

import unittest.mock as mock
import pytest
import yaml

from models.config_manager import ConfigManager
from models.group_data import GroupData
from models.service_data import ServiceData


class TestBase(unittest.TestCase):
    config = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = ConfigManager()
        cls.config.init_configs("../config.ini")

    @pytest.fixture(autouse=True)
    def prepare_client_fixture(self, client):
        self.client_fixture = client

    def assert_exception(self, function, exception, msg_expected: str):
        with self.assertRaises(exception) as context:
            function()
            self.assertEqual(f"{context.exception}", msg_expected)


class TestUnitBase(TestBase):
    def setUp(self):
        super().setUp()
        # mocks
        self.get_yaml_patcher = mock.patch("clients.yaml_parser_client.YamlParserClient.get_yaml")
        self.mock_get_yaml = self.get_yaml_patcher.start()
        self.mock_get_yaml.side_effect = self.__mock_get_yaml

        self.get_html_patcher = mock.patch("clients.html_parser_client.HtmlParserClient.get_html")
        self.mock_get_html = self.get_html_patcher.start()
        self.mock_get_html.side_effect = self.__mock_get_html

        self.get_all_flows_patcher = mock.patch("clients.smart_tests_client.SmartTestsClient.get_all_flows_stats")
        self.mock_get_all_flows = self.get_all_flows_patcher.start()
        self.mock_get_all_flows.side_effect = self.__mock_get_all_flows

        self.analyze_flows_patcher = mock.patch("clients.smart_tests_client.SmartTestsClient.analyze_flows")
        self.mock_analyze_flows = self.analyze_flows_patcher.start()
        self.mock_analyze_flows.side_effect = self.__mock_analyze_flows

    def tearDown(self):
        self.get_yaml_patcher.stop()
        self.get_html_patcher.stop()
        self.get_all_flows_patcher.stop()
        self.analyze_flows_patcher.stop()

    def assert_services_map_entry(self, entry, old_version: str, new_version: str):
        self.assertIsInstance(entry, ServiceData)
        self.assertEqual(entry.old_version, old_version)
        self.assertEqual(entry.new_version, new_version)

    def assert_group_data(self, group_data: GroupData, name: str, path: str, total_count: int):
        self.assertIsNotNone(group_data)
        self.assertEqual(group_data.test_xml_name, name)
        self.assertEqual(group_data.test_xml_path, path)
        self.assertEqual(group_data.total_flows_count, total_count)

    @staticmethod
    def __mock_get_yaml(*args, **kwargs):
        file_name = None
        if args[0] == "http://illin5589:28080/repository/ms-helm-release/index.yaml":
            file_name = "resources/endpoints/index.yaml"
        elif args[0] == "http://test.com/index.yaml":
            file_name = "resources/index.yaml"
        elif args[0] == "http://test2.com/index.yaml":
            file_name = "resources/index_without_filtered.yaml"
        elif args[0] == "http://test3.com/index.yaml":
            file_name = "resources/index_with_configurator_only.yaml"
        elif args[0] == "http://test4.com/index.yaml":
            file_name = "resources/index_without_entries.yaml"

        if file_name:
            with open(file_name, mode="r") as f:
                return yaml.safe_load(f.read())
        else:
            return None

    @staticmethod
    def __mock_get_html(*args, **kwargs):
        file_to_open = None
        if args[0] == "http://example.com/file.zip":
            file_to_open = "resources/build_report.html"
        elif args[0] == "http://test_html_same_version/zipfile.zip":
            file_to_open = "resources/endpoints/build_report_same_versions.html"
        elif args[0] == ("http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4-include-ed/lastSuccessfulBuild"
                         "/BuildReport/*zip*/BuildReport.zip"):
            file_to_open = "resources/endpoints/build_report.html"
        elif args[0] == "http://example.com/missing_table_file.zip":
            file_to_open = "resources/build_report_missing_table.html"

        if file_to_open:
            with open(file_to_open) as f:
                return f.read()
        else:
            return None

    @staticmethod
    def __mock_get_all_flows(*args, **kwargs):
        with open("resources/all_flows_stats.json", mode="r") as f:
            return json.load(f)

    @staticmethod
    def __mock_analyze_flows(*args, **kwargs):
        file_name = None
        if args[0] == "service1":
            file_name = "resources/analyze_services1.json"
        elif args[0] == "service2":
            file_name = "resources/analyze_services2.json"
        elif args[0] == "productconfigurator":
            file_name = "resources/endpoints/smart_stats.json"

        if file_name:
            with open(file_name, mode="r") as f:
                return json.load(f)
        else:
            return None
