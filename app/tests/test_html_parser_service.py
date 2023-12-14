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
        services_map = ServicesData()

        service.load_html("http://example.com/file.zip",
                          services_map,
                          self.config.get_supported_groups().get_item('oc-cd-group4').ms_list)

        self.mock_get_html.assert_called()
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

        service = HtmlParserService()
        services_map = ServicesData()

        self.assert_exception(lambda: service.load_html("http://example.com/missing_table_file.zip",
                                                        services_map,
                                                        self.config.get_supported_groups().get_item('oc-cd-group4')
                                                        .ms_list),
                              NotFoundError,
                              'error with build report structure. not found main deployment table')

        self.mock_get_html.assert_called()
        self.assertEqual(len(services_map), 0)

    def test_load_html_services_map_contains_common_entry(self):
        service = HtmlParserService()
        services_map = ServicesData()
        services_map.add_item("productconfigurator-action",
                                 ServiceData.create().to_version("0.67.6").from_version("0.67.9").build())

        services_map.add_item("productconfigurator-commitmentterm",
                                 ServiceData.create().to_version("0.67.1").from_version("0.67.10").build())

        service.load_html("http://example.com/file.zip",
                          services_map,
                          self.config.get_supported_groups().get_item('oc-cd-group4').ms_list)

        self.mock_get_html.assert_called()
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

    def __assert_entry(self, services_map: ServicesData, key_name: str, old_version: str, new_version: str):
        self.assertIn(key_name, services_map)
        self.assertIsInstance(services_map.get_item(key_name), ServiceData)
        self.assertEqual(services_map.get_item(key_name).to_version, old_version)
        self.assertEqual(services_map.get_item(key_name).from_version, new_version)
