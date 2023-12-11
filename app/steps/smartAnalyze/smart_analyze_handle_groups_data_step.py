from __future__ import annotations

from app import app_main_logger
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.services.smart_test_analyze_service import SmartTestsAnalyzeService
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class InitGroupsDataStep(SmartAnalyzeStepInterface):
    def __init__(self):
        self.client = SmartTestsAnalyzeService()

    def execute(self, parameters: AnalyzeAppServiceParameters):
        app_main_logger.debug("InitGroupsDataStep.execute(): start")

        if parameters is None:
            app_main_logger.warning("InitGroupsDataStep.execute(): Init groups data step. parameters is None.")
            return

        groups_data = self.client.get_all_flows_by_filter(parameters.data_manager.filter_for_curr_group)

        app_main_logger.debug(f"InitGroupsDataStep.execute(): groups_data={groups_data}")

        parameters.data_manager.groups_data = groups_data


class AnalyzeFlowsStep(SmartAnalyzeStepInterface):
    def __init__(self):
        self.client = SmartTestsAnalyzeService()

    def execute(self, parameters: AnalyzeAppServiceParameters):
        app_main_logger.debug("AnalyzeFlowsStep.execute(): Analyze flows step.")

        if parameters is None or parameters.data_manager.groups_data is None:
            return

        self.client.analyze_flows(parameters.data_manager.services_map,
                                  parameters.data_manager.filter_for_curr_group,
                                  parameters.data_manager.groups_data)
