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
        parameters.data_manager.groups_data = {}
        parameters.data_manager.services_map = {}
        self.step.execute(parameters)
        self.assertIsNotNone(parameters.smart_app_service_response)
        self.assertEqual(0, parameters.smart_app_service_response.total_flows_count)
        self.assertEqual(0, parameters.smart_app_service_response.curr_flows_count)
        self.assertEqual({}, parameters.smart_app_service_response.groups)
        self.assertEqual({}, parameters.smart_app_service_response.services)

    def test_execute_with_valid_parameters(self):
        parameters = AnalyzeAppServiceParameters()
        parameters.data_manager.groups_data = {
            'group1': GroupData.create().total_flows_count(10).flows(['flow1', 'flow2']).build(),
            'group2': GroupData.create().total_flows_count(20).flows(['flow3', 'flow4', 'flow5']).build(),
            'group3': GroupData.create().total_flows_count(30).build(),
        }
        parameters.data_manager.services_map = {
            'service1': ServiceData.create().flows(['flow1']).from_version("0.67.110").to_version("0.67.109").build(),
        }

        self.step.execute(parameters)

        self.assertIsNotNone(parameters.smart_app_service_response)
        self.assertEqual(parameters.smart_app_service_response.total_flows_count, 60)
        self.assertEqual(parameters.smart_app_service_response.curr_flows_count, 5)
        self.assertEqual(parameters.smart_app_service_response.groups, {
            'group1': parameters.data_manager.groups_data['group1'].serialize(),
            'group2': parameters.data_manager.groups_data['group2'].serialize(),
            'group3': parameters.data_manager.groups_data['group3'].serialize(),
        })
        self.assertEqual(parameters.smart_app_service_response.services, {
            'service1': parameters.data_manager.services_map['service1'].serialize(),
        })