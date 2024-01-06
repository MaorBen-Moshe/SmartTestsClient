from app.enums.res_info_level import ResInfoLevelEnum
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.models.dto.service_data_dto import ServiceDataDTO
from app.models.group_data import GroupData
from app.models.service_data import ServiceData
from app.steps.smartAnalyze.smart_analyze_prepare_response_step import PrepareResponseStep
from app.tests.test_base import TestBase


class TestSmartAnalyzePrepareResponseStep(TestBase):
    def setUp(self):
        super().setUp()
        self.step = PrepareResponseStep()

    def test_execute_with_empty_groups_data(self):
        parameters = AnalyzeAppServiceParameters()
        parameters.supported_groups = self.config.get_supported_groups()
        parameters.group_name = "oc-cd-group4"

        self.step.execute(parameters)
        self.assertIsNotNone(parameters.smart_app_service_response)
        self.assertEqual(0, parameters.smart_app_service_response.total_flows_count)
        self.assertEqual(0, parameters.smart_app_service_response.curr_flows_count)
        self.assertEqual({}, parameters.smart_app_service_response.groups)
        self.assertEqual([], parameters.smart_app_service_response.services)

    def test_execute_with_valid_parameters_info_level(self):
        parameters = AnalyzeAppServiceParameters()
        parameters.res_info_level = ResInfoLevelEnum.INFO
        parameters.supported_groups = self.config.get_supported_groups()
        parameters.group_name = "oc-cd-group4"

        parameters.groups_data.add_item("group1",
                                        GroupData.create().total_flows_count(10).flows(['flow1', 'flow2']).build())

        parameters.groups_data.add_item("group2",
                                        GroupData.create().total_flows_count(20).flows(
                                            ['flow3', 'flow4', 'flow5']).build())

        parameters.groups_data.add_item("group3",
                                        GroupData.create().total_flows_count(30).build())

        self.step.execute(parameters)

        self.assertIsNotNone(parameters.smart_app_service_response)
        self.assertEqual(parameters.smart_app_service_response.total_flows_count, 60)
        self.assertEqual(parameters.smart_app_service_response.curr_flows_count, 5)

        self.assertEqual(3, len(parameters.smart_app_service_response.groups))
        self.assertEqual(parameters.smart_app_service_response.groups['group1'].toJSON(),
                         parameters.groups_data.get_item('group1').toJSON())

        self.assertEqual(parameters.smart_app_service_response.groups['group2'].toJSON(),
                         parameters.groups_data.get_item('group2').toJSON())

        self.assertEqual(parameters.smart_app_service_response.groups['group3'].toJSON(),
                         parameters.groups_data.get_item('group3').toJSON())

    def test_execute_with_valid_parameters_debug_level(self):
        parameters = AnalyzeAppServiceParameters()
        parameters.res_info_level = ResInfoLevelEnum.DEBUG
        parameters.supported_groups = self.config.get_supported_groups()
        parameters.group_name = "oc-cd-group4"

        parameters.groups_data.add_item("group1",
                                        GroupData.create().total_flows_count(10).flows(['flow1', 'flow2']).build())

        parameters.groups_data.add_item("group2",
                                        GroupData.create().total_flows_count(20).flows(
                                            ['flow3', 'flow4', 'flow5']).build())

        parameters.groups_data.add_item("group3",
                                        GroupData.create().total_flows_count(30).build())

        self.step.execute(parameters)

        self.assertIsNotNone(parameters.smart_app_service_response)
        self.assertEqual(parameters.smart_app_service_response.total_flows_count, 60)
        self.assertEqual(parameters.smart_app_service_response.curr_flows_count, 5)

        self.assertEqual(3, len(parameters.smart_app_service_response.groups))
        self.assertEqual(parameters.smart_app_service_response.groups['group1'].toJSON(),
                         parameters.groups_data.get_item('group1').toJSON())

        self.assertEqual(parameters.smart_app_service_response.groups['group2'].toJSON(),
                         parameters.groups_data.get_item('group2').toJSON())

        self.assertEqual(parameters.smart_app_service_response.groups['group3'].toJSON(),
                         parameters.groups_data.get_item('group3').toJSON())

        self.assertEqual(12, len(parameters.smart_app_service_response.services))
