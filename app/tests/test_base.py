import json
import unittest
import unittest.mock as mock

import pytest

from app import config
from app.models.group_data import GroupData
from app.models.service_data import ServiceData


class TestBase(unittest.TestCase):
    config = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = config

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
        self.nexus_search_patcher = mock.patch("app.clients.nexus_client.NexusClient.search_data")
        self.mock_nexus_search = self.nexus_search_patcher.start()
        self.mock_nexus_search.side_effect = self.__mock_search_data

        self.get_html_patcher = mock.patch("app.clients.html_parser_client.HtmlParserClient.get_html")
        self.mock_get_html = self.get_html_patcher.start()
        self.mock_get_html.side_effect = self.__mock_get_html

        self.get_all_flows_patcher = mock.patch("app.clients.smart_tests_client.SmartTestsClient.get_all_flows_stats")
        self.mock_get_all_flows = self.get_all_flows_patcher.start()
        self.mock_get_all_flows.side_effect = self.__mock_get_all_flows

        self.analyze_flows_patcher = mock.patch("app.clients.smart_tests_client.SmartTestsClient.analyze_flows")
        self.mock_analyze_flows = self.analyze_flows_patcher.start()
        self.mock_analyze_flows.side_effect = self.__mock_analyze_flows

    def tearDown(self):
        super().tearDown()
        self.nexus_search_patcher.stop()
        self.get_html_patcher.stop()
        self.get_all_flows_patcher.stop()
        self.analyze_flows_patcher.stop()

    def assert_services_map_entry(self, entry, to_version: str, from_version: str):
        self.assertIsInstance(entry, ServiceData)
        self.assertEqual(entry.to_version, to_version)
        self.assertEqual(entry.from_version, from_version)

    def assert_group_data(self, group_data: GroupData, name: str, path: str, total_count: int):
        self.assertIsNotNone(group_data)
        self.assertEqual(group_data.test_xml_name, name)
        self.assertEqual(group_data.test_xml_path, path)
        self.assertEqual(group_data.total_flows_count, total_count)

    @staticmethod
    def __mock_search_data(*args, **kwargs):
        name = args[0]['name']
        file_name = None
        if name == "productconfigurator":
            file_name = "resources/nexus_search/configurator_nexus_search_res.json"
        elif name == "productconfigurator-pioperations":
            file_name = "resources/nexus_search/pioperations_nexus_search_res.json"
        elif name == "empty_entry":
            file_name = "resources/nexus_search/empty_nexus_search_res.json"
        elif name == "productconfigurator-missing_version":
            file_name = "resources/nexus_search/configurator_missing_version_nexus_search_res.json"

        if file_name:
            with open(file_name, mode="r") as f:
                return json.load(f)
        else:
            return None

    @staticmethod
    def __mock_get_html(*args, **kwargs):
        file_to_open = None
        if args[0] == "http://example.com/file.zip":
            file_to_open = "resources/html_parse/build_report.html"
        elif args[0] == "http://test_html_same_version/zipfile.zip":
            file_to_open = "resources/endpoints/build_report_same_versions.html"
        elif args[0] == ("http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4/lastSuccessfulBuild"
                         "/BuildReport/*zip*/BuildReport.zip"):
            file_to_open = "resources/endpoints/build_report.html"
        elif args[0] == "http://example.com/missing_table_file.zip":
            file_to_open = "resources/html_parse/build_report_missing_table.html"

        if file_to_open:
            with open(file_to_open) as f:
                return f.read()
        else:
            return None

    @staticmethod
    def __mock_get_all_flows(*args, **kwargs):
        with open("resources/analyze_flows/all_flows_stats.json", mode="r") as f:
            return json.load(f)

    @staticmethod
    def __mock_analyze_flows(*args, **kwargs):
        file_name = None
        if args[0] == "service1":
            file_name = "resources/analyze_flows/analyze_services1.json"
        elif args[0] == "service2":
            file_name = "resources/analyze_flows/analyze_services2.json"
        elif args[0] == "productconfigurator":
            file_name = "resources/endpoints/smart_stats.json"

        if file_name:
            with open(file_name, mode="r") as f:
                return json.load(f)
        else:
            return None
