import responses

from tests.test_base import TestBase
from steps.init_services_data_step import InitServiceMapStep


class TestInitServicesMapStep(TestBase):

    @responses.activate
    def test_init_services_map_success(self):
        path = "http://test.com/yaml"
        with open("resources/index.yaml", mode="r") as f:
            responses.add(responses.GET, path, body=f.read(), status=200)

        services_map = InitServiceMapStep.init_services_map([path])

        assert len(services_map) == 10
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

    @responses.activate
    def test_init_services_map_success_2_paths(self):
        path = "http://test.com/yaml"
        with open("resources/index.yaml", mode="r") as f:
            responses.add(responses.GET, path, body=f.read(), status=200)

        path2 = "http://test2.com/yaml"
        with open("resources/index_without_filtered.yaml", mode="r") as f:
            responses.add(responses.GET, path2, body=f.read(), status=200)

        services_map = InitServiceMapStep.init_services_map([path, path2])

        assert len(services_map) == 10
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

    @responses.activate
    def test_init_services_map_success_2_paths_have_common_entries(self):
        path = "http://test.com/yaml"
        with open("resources/index.yaml", mode="r") as f:
            responses.add(responses.GET, path, body=f.read(), status=200)

        path2 = "http://test2.com/yaml"
        with open("resources/index_with_configurator_only.yaml", mode="r") as f:
            responses.add(responses.GET, path2, body=f.read(), status=200)

        services_map = InitServiceMapStep.init_services_map([path, path2])

        assert len(services_map) == 10
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

    def test_init_services_map_success_empty_paths_list(self):
        services_map = InitServiceMapStep.init_services_map([])

        assert len(services_map) == 0
