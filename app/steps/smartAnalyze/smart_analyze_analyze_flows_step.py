from __future__ import annotations

from app import app_main_logger
from app.decorators.decorators import log_around
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.services.smart_test_analyze_service import SmartTestsAnalyzeService
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class AnalyzeFlowsStep(SmartAnalyzeStepInterface):
    def __init__(self):
        self.client = SmartTestsAnalyzeService()

    @log_around(print_output=False)
    def execute(self, parameters: AnalyzeAppServiceParameters):
        if parameters is None or parameters.groups_data is None:
            return

        self.client.analyze_flows(parameters.services_map,
                                  parameters.curr_group_data.test_files,
                                  parameters.groups_data)

        app_main_logger.debug(f"AnalyzeFlowsStep.execute(): services={parameters.services_map}")
