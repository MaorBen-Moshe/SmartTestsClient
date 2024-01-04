from typing import Iterable

from parameterized import parameterized

from app.exceptions.excpetions import EmptyInputError
from app.models.service_data import ServiceData
from app.models.services_data import ServicesData
from app.services.nexus_search_service import NexusSearchService
from test_base import TestUnitBase


class TestNexusSearchService(TestUnitBase):
    def setUp(self):
        super().setUp()
        self.nexus_search_service = NexusSearchService()
        self._repo = self.config.get_index_data_repository()

    def tearDown(self):
        super().tearDown()
        self.nexus_search_service.services_map = {}

    def test_get_services_master_version_success(self):
        group4 = self.config.get_supported_groups().get_item('oc-cd-group4')

        ms_list = self._get_ms_list_from_services_data(group4.services_data, lambda service: True)

        services_map = self.nexus_search_service.get_services_master_version(self._repo, ms_list)

        self.mock_nexus_search.assert_called()
        self.assertEqual(len(services_map), 2)
        self.assert_services_map_entry(services_map.get_item("productconfigurator-pioperations"),
                                       '0.67.13',
                                       '0.67.13',
                                       group4.project)
        self.assert_services_map_entry(services_map.get_item("productconfigurator"),
                                       '0.67.19',
                                       '0.67.19',
                                       group4.project)

    def test_get_services_master_version_without_items(self):
        service_data = ServiceData.create().service_name("empty_entry").build()
        services_map = self.nexus_search_service.get_services_master_version(self._repo, [service_data])

        self.mock_nexus_search.assert_called()
        self.assertEqual(len(services_map), 0)

    @parameterized.expand([
        ([],),
        None
    ])
    def test_get_services_master_version_empty_input(self, filtered_list):
        services_map = self.nexus_search_service.get_services_master_version(self._repo, filtered_list)

        self.mock_nexus_search.assert_not_called()
        self.assertEqual(len(services_map), 0)

    def test_get_services_master_version_none_input(self):
        self.assert_exception(lambda: self.nexus_search_service.get_services_master_version(
            None,
            self.config.get_supported_groups().get_item('oc-cd-group4').services_data),
                              EmptyInputError,
                              "Provided to 'get_services_master_version' repository=None")

        self.mock_nexus_search.assert_not_called()

    def test_get_services_master_version_duplicate_filtered_list(self):
        ms_list = self._get_ms_list_from_services_data(
            self.config.get_supported_groups().get_item('oc-cd-group4').services_data,
            lambda service: service in ["productconfigurator",
                                        "productconfigurator"])

        services_map = self.nexus_search_service.get_services_master_version(self._repo, ms_list)
        self.assertEqual(len(services_map), 1)
        self.assert_services_map_entry(services_map.get_item("productconfigurator"),
                                       '0.67.19',
                                       '0.67.19',
                                       "DIGOC")

    def test_get_services_master_version_missing_version(self):
        service_data = ServiceData.create().service_name("productconfigurator-missing_version").build()
        services_map = self.nexus_search_service.get_services_master_version(self._repo,
                                                                             [service_data])
        self.mock_nexus_search.assert_called()
        self.assertEqual(len(services_map), 0)

    @staticmethod
    def _get_ms_list_from_services_data(services_data: ServicesData, filter_ms) -> Iterable[ServiceData]:
        return (services_data.get_item(service) for service in services_data if filter_ms(service))
