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

    def test_update_services_master_version_success(self):
        group4 = self.config.get_supported_groups().get_item('oc-cd-group4')

        ms_list = self._get_ms_list_from_services_data(group4.services_data, lambda service: True)

        self.nexus_search_service.update_services_master_version(self._repo, ms_list)

        self.mock_nexus_search.assert_called()
        self.assertEqual(len(group4.services_data), 12)
        self.assert_services_map_entry(group4.services_data.get_item("productconfigurator-pioperations"),
                                       '0.67.13',
                                       '0.67.13',
                                       group4.project)
        self.assert_services_map_entry(group4.services_data.get_item("productconfigurator"),
                                       '0.67.19',
                                       '0.67.19',
                                       group4.project)

    def test_update_services_master_version_without_items(self):
        service_data = ServiceData.create().service_name("empty_entry").build()
        self.nexus_search_service.update_services_master_version(self._repo, [service_data])

        self.mock_nexus_search.assert_called()
        self.assertIsNotNone(service_data)
        self.assertIsNone(service_data.to_version)
        self.assertIsNone(service_data.from_version)

    @parameterized.expand([
        ([],),
        None
    ])
    def test_update_services_master_version_empty_input(self, filtered_list):
        self.nexus_search_service.update_services_master_version(self._repo, filtered_list)

        self.mock_nexus_search.assert_not_called()

    def test_update_services_master_version_none_input(self):
        self.assert_exception(lambda: self.nexus_search_service.update_services_master_version(
            None,
            self.config.get_supported_groups().get_item('oc-cd-group4').services_data),
                              EmptyInputError,
                              "Provided to 'update_services_master_version' repository=None")

        self.mock_nexus_search.assert_not_called()

    def test_update_services_master_version_duplicate_filtered_list(self):
        group4 = self.config.get_supported_groups().get_item('oc-cd-group4')
        ms_list = self._get_ms_list_from_services_data(
            group4.services_data,
            lambda service: service in ["productconfigurator",
                                        "productconfigurator"])

        self.nexus_search_service.update_services_master_version(self._repo, ms_list)
        self.assertEqual(len(group4.services_data), 12)
        self.assert_services_map_entry(group4.services_data.get_item("productconfigurator"),
                                       '0.67.19',
                                       '0.67.19',
                                       "DIGOC")

    def test_update_services_master_version_missing_version(self):
        service_data = ServiceData.create().service_name("productconfigurator-missing_version").build()
        self.nexus_search_service.update_services_master_version(self._repo,
                                                                 [service_data])
        self.mock_nexus_search.assert_called()
        self.assertIsNotNone(service_data)
        self.assertIsNone(service_data.to_version)
        self.assertIsNone(service_data.from_version)

    @staticmethod
    def _get_ms_list_from_services_data(services_data: ServicesData, filter_ms) -> Iterable[ServiceData]:
        return (services_data.get_item(service) for service in services_data if filter_ms(service))
