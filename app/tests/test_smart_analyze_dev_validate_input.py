from __future__ import annotations

from parameterized import parameterized

from app.exceptions.excpetions import BadRequest
from app.mappers.service_data_mapper import ServiceDataMapper
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.dto.service_data_dto import ServiceDataDTO
from app.models.service_data import ServiceData
from app.models.services_data import ServicesData
from app.steps.smartAnalyzeDev.smart_analyze_dev_validate_input import SmartAnalyzeDevValidateInputStep
from app.tests.test_base import TestUnitBase


class TestSmartAnalyzeDevValidateInputUnit(TestUnitBase):

    def setUp(self) -> None:
        super().setUp()
        self.step = SmartAnalyzeDevValidateInputStep()

    @parameterized.expand([
        ServiceDataDTO.create().service_name("service1").from_version("from1").build(),
        ServiceDataDTO.create().service_name("service2").pull_request_id("pull_request_id").build(),
    ])
    def test_check_input_success(self, service_data_dto: ServiceDataDTO | None):
        try:
            services_data = ServicesData()
            if service_data_dto:
                services_data.add_item(service_data_dto.service_name, ServiceDataMapper.map_from_dto(service_data_dto))
            parameters = AnalyzeDevAppServiceParameters.create().services_map(services_data).build()
            parameters.supported_groups = self.config.get_supported_groups()
            self.step.execute(parameters)
            if service_data_dto:
                self.assertIsNotNone(parameters.services_map)
                self.assertEqual(1, len(parameters.services_map))
                self.assertIsNotNone(parameters.services_map.get_item(service_data_dto.service_name))
                self.assertEqual(service_data_dto.from_version,
                                 parameters.services_map.get_item(service_data_dto.service_name).from_version)
                self.assertEqual(service_data_dto.to_version,
                                 parameters.services_map.get_item(service_data_dto.service_name).to_version)
                self.assertEqual(service_data_dto.pull_request_id,
                                 parameters.services_map.get_item(service_data_dto.service_name).pull_request_id)
        except Exception as ex:
            self.fail(f"Error: {ex}")

    @parameterized.expand([
        (None,),
        ('service1',),
        ([None],),
        (['service1'],),
        ([ServiceDataDTO.create().from_version("from1").build()],),
    ])
    def test_check_input_wrong_services_provided(self, service_data_dto):
        services_dto = ServiceDataMapper.map_from_dict_list_to_dto(service_data_dto)

        parameters = (AnalyzeDevAppServiceParameters.create()
                      .services_map(ServiceDataMapper.map_from_dto_to_services_data(services_dto)).build())

        self.step.execute(parameters)

        self.assertIsNotNone(parameters)
        self.assertIsNotNone(parameters.services_map)
        self.assertEqual(0, len(parameters.services_map))

    def test_check_input_missing_from_and_no_pr_provided(self):
        services_data = ServicesData()
        services_data.add_item("service1", ServiceData.create().build())
        parameters = AnalyzeDevAppServiceParameters.create().services_map(services_data).build()
        self.assert_exception(lambda: self.step.execute(parameters),
                              BadRequest,
                              "Service is missing mandatory field: 'from'.")

    def test_check_input_from_with_pr_id_provided(self):
        services_data = ServicesData()
        services_data.add_item("service1", ServiceData.create()
                               .from_version("from1")
                               .to_version("to1")
                               .pull_request_id("pr_id").build())
        parameters = AnalyzeDevAppServiceParameters.create().services_map(services_data).build()

        self.step.execute(parameters)

        self.assertIsNotNone(parameters)
        self.assertIsNotNone(parameters.services_map)
        self.assertEqual(1, len(parameters.services_map))
        self.assertIsNotNone(parameters.services_map.get_item("service1"))
        self.assertIsNone(parameters.services_map.get_item("service1").from_version)
        self.assertIsNone(parameters.services_map.get_item("service1").to_version)
        self.assertEqual("pr_id", parameters.services_map.get_item("service1").pull_request_id)

    def test_check_input_wrong_project_provided(self):
        services_data = ServicesData()
        services_data.add_item("productconfigurator", ServiceData.create()
                               .from_version("from1")
                               .to_version("to1")
                               .project("wrong_project").build())
        parameters = AnalyzeDevAppServiceParameters.create().services_map(services_data).build()
        parameters.supported_groups = self.config.get_supported_groups()
        self.step.execute(parameters)
        self.assertIsNotNone(parameters)
        self.assertIsNotNone(parameters.services_map)
        self.assertEqual(1, len(parameters.services_map))
        self.assertIsNotNone(parameters.services_map.get_item("productconfigurator"))
        self.assertEqual("DIGOC", parameters.services_map.get_item("productconfigurator").project)