from exceptions.excpetions import EmptyInputError
from services.yaml_parser_service import YamlParserService
from tests.test_base import UnitTestBase


class TestYamlParserService(UnitTestBase):
    def setUp(self):
        super().setUp()
        self.yaml_parser_service = YamlParserService()

    def tearDown(self):
        self.yaml_parser_service.services_map = {}

    def test_request_yaml_external_success(self):
        path = "http://test.com/index.yaml"

        services_map = self.yaml_parser_service.request_yaml_external([path])

        self.mock_get_yaml.assert_called()
        self.assertEqual(len(services_map), 10)
        self.assert_services_map_entry(services_map.get("productconfigurator-qualification"),
                                       '0.67.9',
                                       '0.67.9')
        self.assert_services_map_entry(services_map.get("productconfigurator-pioperations"),
                                       '0.67.9',
                                       '0.67.9')
        self.assert_services_map_entry(services_map.get("productconfigurator-action"),
                                       '0.67.8',
                                       '0.67.8')
        self.assert_services_map_entry(
            services_map.get("productconfigurator-commitmentterm"),
            '0.67.10',
            '0.67.10')
        self.assert_services_map_entry(services_map.get("productconfigurator-promotion"),
                                       '0.67.17',
                                       '0.67.17')
        self.assert_services_map_entry(services_map.get("productconfigurator-price"),
                                       '0.67.13',
                                       '0.67.13')
        self.assert_services_map_entry(services_map.get("productconfigurator-mergeentities"),
                                       '1.67.11',
                                       '1.67.11')
        self.assert_services_map_entry(services_map.get("productconfigurator-replace"),
                                       '0.67.11',
                                       '0.67.11')
        self.assert_services_map_entry(services_map.get("productvalidator"),
                                       '0.67.29',
                                       '0.67.29')
        self.assert_services_map_entry(services_map.get("productconfigurator"),
                                       '0.67.14',
                                       '0.67.14')

    def test_request_yaml_external_input_without_filtered_entries(self):
        path = "http://test2.com/index.yaml"

        services_map = self.yaml_parser_service.request_yaml_external([path])

        self.mock_get_yaml.assert_called()
        self.assertEqual(len(services_map), 0)

    def test_request_yaml_external_yaml_without_entries(self):
        path = "http://test4.com/index.yaml"

        services_map = self.yaml_parser_service.request_yaml_external([path])

        self.mock_get_yaml.assert_called()
        self.assertEqual(len(services_map), 0)

    def test_request_yaml_external_empty_body(self):
        path = "http://test5.com/index.yaml"

        services_map = self.yaml_parser_service.request_yaml_external([path])

        self.mock_get_yaml.assert_called()
        self.assertEqual(len(services_map), 0)

    def test_init_services_map_success_2_paths(self):
        path = "http://test.com/index.yaml"
        path2 = "http://test2.com/index.yaml"

        services_map = self.yaml_parser_service.request_yaml_external([path, path2])

        self.assertEqual(self.mock_get_yaml.call_count, 2)
        self.assertEqual(len(services_map), 10)
        self.assert_services_map_entry(services_map.get("productconfigurator-qualification"),
                                       '0.67.9',
                                       '0.67.9')
        self.assert_services_map_entry(services_map.get("productconfigurator-pioperations"),
                                       '0.67.9',
                                       '0.67.9')
        self.assert_services_map_entry(services_map.get("productconfigurator-action"),
                                       '0.67.8',
                                       '0.67.8')
        self.assert_services_map_entry(
            services_map.get("productconfigurator-commitmentterm"),
            '0.67.10',
            '0.67.10')
        self.assert_services_map_entry(services_map.get("productconfigurator-promotion"),
                                       '0.67.17',
                                       '0.67.17')
        self.assert_services_map_entry(services_map.get("productconfigurator-price"),
                                       '0.67.13',
                                       '0.67.13')
        self.assert_services_map_entry(services_map.get("productconfigurator-mergeentities"),
                                       '1.67.11',
                                       '1.67.11')
        self.assert_services_map_entry(services_map.get("productconfigurator-replace"),
                                       '0.67.11',
                                       '0.67.11')
        self.assert_services_map_entry(services_map.get("productvalidator"),
                                       '0.67.29',
                                       '0.67.29')
        self.assert_services_map_entry(services_map.get("productconfigurator"),
                                       '0.67.14',
                                       '0.67.14')

    def test_init_services_map_success_2_paths_have_common_entries(self):
        path = "http://test.com/index.yaml"
        path2 = "http://test3.com/index.yaml"

        services_map = self.yaml_parser_service.request_yaml_external([path, path2])

        self.assertEqual(self.mock_get_yaml.call_count, 2)
        self.assertEqual(len(services_map), 10)
        self.assert_services_map_entry(services_map.get("productconfigurator-qualification"),
                                       '0.67.9',
                                       '0.67.9')
        self.assert_services_map_entry(services_map.get("productconfigurator-pioperations"),
                                       '0.67.9',
                                       '0.67.9')
        self.assert_services_map_entry(services_map.get("productconfigurator-action"),
                                       '0.67.8',
                                       '0.67.8')
        self.assert_services_map_entry(
            services_map.get("productconfigurator-commitmentterm"),
            '0.67.10',
            '0.67.10')
        self.assert_services_map_entry(services_map.get("productconfigurator-promotion"),
                                       '0.67.17',
                                       '0.67.17')
        self.assert_services_map_entry(services_map.get("productconfigurator-price"),
                                       '0.67.13',
                                       '0.67.13')
        self.assert_services_map_entry(services_map.get("productconfigurator-mergeentities"),
                                       '1.67.11',
                                       '1.67.11')
        self.assert_services_map_entry(services_map.get("productconfigurator-replace"),
                                       '0.67.11',
                                       '0.67.11')
        self.assert_services_map_entry(services_map.get("productvalidator"),
                                       '0.67.29',
                                       '0.67.29')
        self.assert_services_map_entry(services_map.get("productconfigurator"),
                                       '0.66.118',
                                       '0.66.118')

    def test_request_yaml_external_empty_input(self):
        services_map = self.yaml_parser_service.request_yaml_external([])

        self.mock_get_yaml.assert_not_called()
        self.assertEqual(len(services_map), 0)

    def test_request_yaml_external_none_input(self):
        self.assert_exception(lambda: self.yaml_parser_service.request_yaml_external(None),
                              EmptyInputError,
                              "Provided to 'request_yaml_external' None urls list")

        self.mock_get_yaml.assert_not_called()
