from parameterized import parameterized

from app.exceptions.excpetions import EmptyInputError
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
        services_map = self.nexus_search_service.get_services_master_version(
            self._repo,
            self.config.get_supported_groups()['oc-cd-group4'].filtered_ms_list)

        self.mock_nexus_search.assert_called()
        self.assertEqual(len(services_map), 2)
        self.assert_services_map_entry(services_map.get("productconfigurator-pioperations"),
                                       '0.67.13',
                                       '0.67.13')
        self.assert_services_map_entry(services_map.get("productconfigurator"),
                                       '0.67.19',
                                       '0.67.19')

    def test_get_services_master_version_without_items(self):
        services_map = self.nexus_search_service.get_services_master_version(self._repo, ["empty_entry"])

        self.mock_nexus_search.assert_called()
        self.assertEqual(len(services_map), 0)

    @parameterized.expand([
        ([],),
        None
    ])
    def test_get_services_master_version_empty_input(self, filtered_list):
        services_map = self.nexus_search_service.get_services_master_version(self._repo,
                                                                             filtered_list)

        self.mock_nexus_search.assert_not_called()
        self.assertEqual(len(services_map), 0)

    def test_get_services_master_version_none_input(self):
        self.assert_exception(lambda: self.nexus_search_service.get_services_master_version(
            None,
            self.config.get_supported_groups()['oc-cd-group4'].filtered_ms_list),
                              EmptyInputError,
                              "Provided to 'get_services_master_version' repository=None")

        self.mock_nexus_search.assert_not_called()

    def test_get_services_master_version_duplicate_filtered_list(self):
        services_map = self.nexus_search_service.get_services_master_version(self._repo,
                                                                             ["productconfigurator",
                                                                              "productconfigurator"])
        self.assertEqual(len(services_map), 1)
        self.assert_services_map_entry(services_map.get("productconfigurator"),
                                       '0.67.19',
                                       '0.67.19')

    def test_get_services_master_version_missing_version(self):
        services_map = self.nexus_search_service.get_services_master_version(self._repo,
                                                                             ["productconfigurator-missing_version"])
        self.mock_nexus_search.assert_called()
        self.assertEqual(len(services_map), 0)
