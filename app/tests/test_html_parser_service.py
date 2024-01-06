from __future__ import annotations

from app.exceptions.excpetions import NotFoundError
from app.models.service_data import ServiceData
from app.models.services_data import ServicesData
from app.services.html_parser_service import HtmlParserService
from test_base import TestUnitBase


class TestHtmlParserServiceUnit(TestUnitBase):

    def setUp(self):
        super().setUp()

    def test_load_html_success(self):
        service = HtmlParserService()
        services_map = self.config.get_supported_groups().get_item('oc-cd-group4').services_data

        service.load_html("http://example.com/file.zip",
                          services_map)

        self.mock_get_html.assert_called()
        self.assertEqual(len(services_map), 12)
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
        self.__assert_entry(services_map, "productconfigurator-subdomain", '0.67.6', '0.67.6')

    def test_load_html_missing_table(self):
        self.mock_get_html.return_value = "<HTML></HTML>"

        service = HtmlParserService()
        services_map = self.config.get_supported_groups().get_item('oc-cd-group4').services_data

        self.assert_exception(lambda: service.load_html("http://example.com/missing_table_file.zip",
                                                        services_map),
                              NotFoundError,
                              'error with build report structure. not found main deployment table')

        self.mock_get_html.assert_called()
        self.assertEqual(len(services_map), 12)
        for service in services_map:
            service_data = services_map.get_item(service)
            self.assertIsNotNone(service_data)
            self.assertIsNone(service_data.from_version)
            self.assertIsNone(service_data.to_version)

    def test_load_html_services_map_contains_common_entry(self):
        service = HtmlParserService()
        services_map = self.config.get_supported_groups().get_item('oc-cd-group4').services_data

        services_map.get_item("productconfigurator-action").to_version = "0.67.6"
        services_map.get_item("productconfigurator-action").from_version = "0.67.9"

        services_map.get_item("productconfigurator-commitmentterm").to_version = "0.67.1"
        services_map.get_item("productconfigurator-commitmentterm").from_version = "0.67.10"

        service.load_html("http://example.com/file.zip",
                          services_map)

        self.mock_get_html.assert_called()
        self.assertEqual(len(services_map), 12)
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
        self.__assert_entry(services_map, "productconfigurator-subdomain", '0.67.6', '0.67.6')

    def test_load_html_empty_services_data(self):
        service = HtmlParserService()
        services_data = ServicesData()

        service.load_html("http://example.com/file.zip",
                          services_data)

        self.assertEqual(len(services_data), 0)

    def __assert_entry(self, services_map: ServicesData, key_name: str, old_version: str, new_version: str):
        self.assertIn(key_name, services_map)
        self.assertIsInstance(services_map.get_item(key_name), ServiceData)
        self.assertEqual(services_map.get_item(key_name).to_version, old_version)
        self.assertEqual(services_map.get_item(key_name).from_version, new_version)
