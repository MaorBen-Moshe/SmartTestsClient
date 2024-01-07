from parameterized import parameterized

from app.models.service_data import ServiceData
from app.models.services_data import ServicesData
from app.services.smart_analyze_dev_update_services_data_service import UpdateServiceDataService
from app.tests.test_base import TestUnitBase


class TestUpdateServiceDataService(TestUnitBase):
    def setUp(self):
        super().setUp()
        self.update_service_data_service = UpdateServiceDataService()
        self._repo = self.config.get_index_data_repository()

    def test_update_services_data_success(self):
        services_data = ServicesData()
        services_data.add_item("productconfigurator",
                               ServiceData.create()
                               .service_name("productconfigurator")
                               .from_version("0.67.21").build())

        with self.app_fixture.test_request_context():
            self.update_service_data_service.update_services_data(self._repo, services_data)

        self.assertIsNotNone(services_data)
        self.assertEqual(len(services_data), 1)
        self.assert_services_map_entry(services_data.get_item("productconfigurator"),
                                       "0.67.19",
                                       "0.67.21",
                                       None)

    def test_update_services_data_one_item_with_missing_to_version(self):
        services_data = ServicesData()
        services_data.add_item("productconfigurator",
                               ServiceData.create()
                               .service_name("productconfigurator")
                               .from_version("0.67.21").build())
        services_data.add_item("productconfigurator-pioperations",
                               ServiceData.create().from_version("0.67.13").to_version("0.67.9").build())

        with self.app_fixture.test_request_context():
            self.update_service_data_service.update_services_data(self._repo, services_data)

        self.mock_nexus_search.assert_called_once()
        self.assertIsNotNone(services_data)
        self.assertEqual(len(services_data), 2)
        self.assert_services_map_entry(services_data.get_item("productconfigurator"),
                                       "0.67.19",
                                       "0.67.21",
                                       None)
        self.assert_services_map_entry(services_data.get_item("productconfigurator-pioperations"),
                                       "0.67.9",
                                       "0.67.13",
                                       None)

    @parameterized.expand([
        ([],),
        None
    ])
    def test_update_services_data_empty_input(self, services_data):
        res = self.update_service_data_service.update_services_data(self._repo, services_data)
        self.assertIsNone(res)

    def test_update_from_template_with_valid_services(self):
        services = ServicesData()
        services.add_item("productconfigurator", ServiceData.create().service_name("productconfigurator")
                          .from_version("0.67.21")
                          .build())

        self.update_service_data_service.update_from_template(services)

        self.assertIsNotNone(services)
        self.assertIn("productconfigurator", services)
        service_data = services.get_item("productconfigurator")
        self.assertIsNotNone(service_data)
        self.assertEqual(service_data.repo_name, "productconfigurator-ms")
        self.assertEqual(service_data.project, "DIGOC")
        self.assertEqual(service_data.related_group, "oc-cd-group4")

    def test_update_from_template_with_project_already(self):
        services = ServicesData()
        services.add_item("productconfigurator", ServiceData.create().service_name("productconfigurator")
                          .from_version("0.67.21")
                          .project("NOT_DIGOC")
                          .build())

        self.update_service_data_service.update_from_template(services)

        # assert that the services are updated correctly
        self.assertIsNotNone(services)
        self.assertIn("productconfigurator", services)
        service_data = services.get_item("productconfigurator")
        self.assertIsNotNone(service_data)
        self.assertEqual(service_data.repo_name, "productconfigurator-ms")
        self.assertEqual(service_data.project, "NOT_DIGOC")
        self.assertEqual(service_data.related_group, "oc-cd-group4")

    def test_update_from_template_with_repo_name_already(self):
        services = ServicesData()
        services.add_item("productconfigurator", ServiceData.create().service_name("productconfigurator")
                          .from_version("0.67.21")
                          .repo_name("repo_name")
                          .build())

        self.update_service_data_service.update_from_template(services)

        # assert that the services are updated correctly
        self.assertIsNotNone(services)
        self.assertIn("productconfigurator", services)
        service_data = services.get_item("productconfigurator")
        self.assertIsNotNone(service_data)
        self.assertEqual(service_data.repo_name, "repo_name")
        self.assertEqual(service_data.project, "DIGOC")
        self.assertEqual(service_data.related_group, "oc-cd-group4")

    def test_update_from_template_with_related_group_already(self):
        services = ServicesData()
        services.add_item("productconfigurator", ServiceData.create().service_name("productconfigurator")
                          .from_version("0.67.21")
                          .related_group("related_group")
                          .build())

        self.update_service_data_service.update_from_template(services)

        # assert that the services are updated correctly
        self.assertIsNotNone(services)
        self.assertIn("productconfigurator", services)
        service_data = services.get_item("productconfigurator")
        self.assertIsNotNone(service_data)
        self.assertEqual(service_data.repo_name, "productconfigurator-ms")
        self.assertEqual(service_data.project, "DIGOC")
        self.assertEqual(service_data.related_group, "related_group")
