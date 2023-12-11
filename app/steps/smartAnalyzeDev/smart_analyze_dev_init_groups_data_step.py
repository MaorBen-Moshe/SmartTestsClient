from __future__ import annotations

from app import app_main_logger
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.services.smart_test_analyze_service import SmartTestsAnalyzeService
from app.steps.smartAnalyzeDev.interfaces.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class InitGroupsDataStep(SmartAnalyzeDevStepInterface):
    def __init__(self):
        self.service = SmartTestsAnalyzeService()

    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        app_main_logger.debug("InitGroupsDataStep.execute(): start")

        if parameters is None or parameters.data_manager is None:
            return

        groups_data = self.service.get_all_flows_by_filter([])

        app_main_logger.debug(f"InitGroupsDataStep.execute(): groups data = {groups_data}")

        parameters.data_manager.groups_data = groups_data
