from app.enums.res_info_level import ResInfoLevelEnum
from app.models.analyze_app_params import AnalyzeAppServiceParameters
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

        self.step.execute(parameters)
        self.assertIsNotNone(parameters.smart_app_service_response)
        self.assertEqual(0, parameters.smart_app_service_response.total_flows_count)
        self.assertEqual(0, parameters.smart_app_service_response.curr_flows_count)
        self.assertEqual({}, parameters.smart_app_service_response.groups)
        self.assertEqual({}, parameters.smart_app_service_response.services)

    def test_execute_with_valid_parameters_info_level(self):
        parameters = AnalyzeAppServiceParameters()
        parameters.res_info_level = ResInfoLevelEnum.INFO

        parameters.groups_data.add_item("group1",
                                        GroupData.create().total_flows_count(10).flows(['flow1', 'flow2']).build())

        parameters.groups_data.add_item("group2",
                                        GroupData.create().total_flows_count(20).flows(
                                            ['flow3', 'flow4', 'flow5']).build())

        parameters.groups_data.add_item("group3",
                                        GroupData.create().total_flows_count(30).build())

        parameters.services_map.add_item("service1",
                                         ServiceData.create().flows(['flow1']).from_version("0.67.110").to_version(
                                             "0.67.109").build())

        self.step.execute(parameters)

        self.assertIsNotNone(parameters.smart_app_service_response)
        self.assertEqual(parameters.smart_app_service_response.total_flows_count, 60)
        self.assertEqual(parameters.smart_app_service_response.curr_flows_count, 5)
        self.assertEqual(parameters.smart_app_service_response.groups, {
            'group1': parameters.groups_data.get_item('group1').toJSON(),
            'group2': parameters.groups_data.get_item('group2').toJSON(),
            'group3': parameters.groups_data.get_item('group3').toJSON(),
        })

    def test_execute_with_valid_parameters_debug_level(self):
        parameters = AnalyzeAppServiceParameters()
        parameters.res_info_level = ResInfoLevelEnum.DEBUG
        parameters.groups_data.add_item("group1",
                                        GroupData.create().total_flows_count(10).flows(['flow1', 'flow2']).build())

        parameters.groups_data.add_item("group2",
                                        GroupData.create().total_flows_count(20).flows(
                                            ['flow3', 'flow4', 'flow5']).build())

        parameters.groups_data.add_item("group3",
                                        GroupData.create().total_flows_count(30).build())

        parameters.services_map.add_item("service1",
                                         ServiceData.create()
                                         .service_name("service1").flows(['flow1']).from_version("0.67.110").to_version(
                                             "0.67.109").build())

        self.step.execute(parameters)

        self.assertIsNotNone(parameters.smart_app_service_response)
        self.assertEqual(parameters.smart_app_service_response.total_flows_count, 60)
        self.assertEqual(parameters.smart_app_service_response.curr_flows_count, 5)
        self.assertEqual(parameters.smart_app_service_response.groups, {
            'group1': parameters.groups_data.get_item('group1').toJSON(),
            'group2': parameters.groups_data.get_item('group2').toJSON(),
            'group3': parameters.groups_data.get_item('group3').toJSON(),
        })
        self.assertEqual(parameters.smart_app_service_response.services, {
            'service1': parameters.services_map.get_item('service1').toJSON(),
        })
