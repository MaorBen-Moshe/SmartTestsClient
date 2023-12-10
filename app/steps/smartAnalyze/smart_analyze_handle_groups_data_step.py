from __future__ import annotations

from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.services.smart_test_analyze_service import SmartTestsAnalyzeService
from app.steps.smartAnalyze.smart_analyze_step_interface import SmartAnalyzeStepInterface


class InitGroupsDataStep(SmartAnalyzeStepInterface):
    def __init__(self):
        self.client = SmartTestsAnalyzeService()

    def execute(self, parameters: AnalyzeAppServiceParameters):
        if parameters is None or parameters.data_manager.filter_for_curr_group is None:
            return

        groups_data = self.client.get_all_flows_by_filter(parameters.data_manager.filter_for_curr_group)

        parameters.data_manager.groups_data = groups_data


class AnalyzeFlowsStep(SmartAnalyzeStepInterface):
    def __init__(self):
        self.client = SmartTestsAnalyzeService()

    def execute(self, parameters: AnalyzeAppServiceParameters):
        if parameters is None or parameters.data_manager.groups_data is None:
            return

        self.client.analyze_flows(parameters.data_manager.services_map,
                                  parameters.data_manager.filter_for_curr_group,
                                  parameters.data_manager.groups_data)
