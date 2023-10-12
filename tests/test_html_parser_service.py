import mock

from exceptions.excpetions import NotFoundError
from models.service_data import ServiceData, ServiceDataBuilder
from services.html_parser_service import HtmlParserService
from tests.test_base import TestBase


class TestHtmlParserService(TestBase):

    def setUp(self):
        super().setUp()
        self.patcher = mock.patch("clients.html_parser_client.HtmlParserClient.get_html")
        self.mock_get_html = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_load_html_success(self):
        with open("resources/build_report.html") as f:
            self.mock_get_html.return_value = f.read()

        service = HtmlParserService("http://example.com/file.zip")
        services_map = {}

        service.load_html(services_map)

        self.assertEqual(len(services_map), 10)
        self.__assert_entry(services_map, "productconfigurator-action", '0.67.8', '0.67.8')
        self.__assert_entry(services_map, "productconfigurator-price", '0.67.15', '0.67.15')
        self.__assert_entry(services_map, "productconfigurator-qualification", '0.67.9', '0.67.9')
        self.__assert_entry(services_map, "productconfigurator-commitmentterm", '0.67.10', '0.67.10')
        self.__assert_entry(services_map, "productconfigurator", '0.67.14', '0.67.14')
        self.__assert_entry(services_map, "productconfigurator-pioperations", '0.67.9', '0.67.9')
        self.__assert_entry(services_map, "productvalidator", '0.67.41', '0.67.41')
        self.__assert_entry(services_map, "productconfigurator-promotion", '0.67.17', '0.67.17')
        self.__assert_entry(services_map, "productconfigurator-replace", '0.67.19', '0.67.19')
        self.__assert_entry(services_map, "productconfigurator-mergeentities", '1.67.13', '1.67.13')

    def test_load_html_missing_table(self):
        self.mock_get_html.return_value = "<HTML></HTML>"

        service = HtmlParserService("http://example.com/file.zip")
        services_map = {}

        self.assert_exception(lambda: service.load_html(services_map),
                              NotFoundError,
                              'error with build report structure. not found main deployment table')

        self.assertEqual(len(services_map), 0)

    def test_load_html_services_map_contains_common_entry(self):
        with open("resources/build_report.html") as f:
            self.mock_get_html.return_value = f.read()

        service = HtmlParserService("http://example.com/file.zip")
        services_map = {
            "productconfigurator-action": ServiceDataBuilder().old_version("0.67.6").new_version("0.67.9").build(),
            "productconfigurator-commitmentterm": ServiceDataBuilder().old_version("0.67.1").new_version(
                "0.67.10").build(),
        }

        service.load_html(services_map)

        self.assertEqual(len(services_map), 10)
        self.__assert_entry(services_map, "productconfigurator-action", '0.67.8', '0.67.9')
        self.__assert_entry(services_map, "productconfigurator-price", '0.67.15', '0.67.15')
        self.__assert_entry(services_map, "productconfigurator-qualification", '0.67.9', '0.67.9')
        self.__assert_entry(services_map, "productconfigurator-commitmentterm", '0.67.10', '0.67.10')
        self.__assert_entry(services_map, "productconfigurator", '0.67.14', '0.67.14')
        self.__assert_entry(services_map, "productconfigurator-pioperations", '0.67.9', '0.67.9')
        self.__assert_entry(services_map, "productvalidator", '0.67.41', '0.67.41')
        self.__assert_entry(services_map, "productconfigurator-promotion", '0.67.17', '0.67.17')
        self.__assert_entry(services_map, "productconfigurator-replace", '0.67.19', '0.67.19')
        self.__assert_entry(services_map, "productconfigurator-mergeentities", '1.67.13', '1.67.13')

    def __assert_entry(self, services_map: dict[str, ServiceData], key_name: str, old_version: str, new_version: str):
        self.assertIn(key_name, services_map)
        self.assertIsInstance(services_map[key_name], ServiceData)
        self.assertEqual(services_map[key_name].old_version, old_version)
        self.assertEqual(services_map[key_name].new_version, new_version)
