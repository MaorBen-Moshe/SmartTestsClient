import responses

from models.service_data import ServiceData
from services.yaml_parser import YamlParserService
from tests.test_base import TestBase


class TestYamlParserService(TestBase):
    def setUp(self):
        super().setUp()
        self.yaml_parser_service = YamlParserService()

    @responses.activate
    def test_request_yaml_external(self):
        path = "http://test.com/yaml"
        with open("resources/index.yaml", mode="r") as f:
            responses.add(responses.GET, path, body=f.read(), status=200)

        services_map = self.yaml_parser_service.request_yaml_external(path)

        assert len(services_map) == 10
        self.__assert_services_map_entry(services_map.get("productconfigurator-qualification"),
                                         '0.67.9')
        self.__assert_services_map_entry(services_map.get("productconfigurator-pioperations"),
                                         '0.67.9')
        self.__assert_services_map_entry(services_map.get("productconfigurator-action"),
                                         '0.67.8')
        self.__assert_services_map_entry(
            services_map.get("productconfigurator-commitmentterm"),
            '0.67.10')
        self.__assert_services_map_entry(services_map.get("productconfigurator-promotion"),
                                         '0.67.17')
        self.__assert_services_map_entry(services_map.get("productconfigurator-price"),
                                         '0.67.13')
        self.__assert_services_map_entry(services_map.get("productconfigurator-mergeentities"),
                                         '1.67.11')
        self.__assert_services_map_entry(services_map.get("productconfigurator-replace"),
                                         '0.67.11')
        self.__assert_services_map_entry(services_map.get("productvalidator"), '0.67.29')
        self.__assert_services_map_entry(services_map.get("productconfigurator"), '0.67.14')

        self.yaml_parser_service.services_map = {}

    @responses.activate
    def test_request_yaml_external_input_without_filtered_entries(self):
        path = "http://test.com/yaml"
        with open("resources/index_without_filtered.yaml", mode="r") as f:
            responses.add(responses.GET, path, body=f.read(), status=200)

        services_map = self.yaml_parser_service.request_yaml_external(path)

        assert len(services_map) == 0

    @responses.activate
    def test_request_yaml_external_yaml_without_entries(self):
        path = "http://test.com/yaml"
        with open("resources/index_without_entries.yaml", mode="r") as f:
            responses.add(responses.GET, path, body=f.read(), status=200)

        services_map = self.yaml_parser_service.request_yaml_external(path)

        assert len(services_map) == 0

    @responses.activate
    def test_request_yaml_external_empty_input(self):
        path = "http://test.com/yaml"
        responses.add(responses.GET, path, body="", status=200)

        services_map = self.yaml_parser_service.request_yaml_external(path)

        assert len(services_map) == 0

    @staticmethod
    def __assert_services_map_entry(entry, version: str):
        assert type(entry) is ServiceData
        assert entry.new_version == entry.old_version == version
