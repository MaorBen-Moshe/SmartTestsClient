from __future__ import annotations

from app import app_main_logger
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.services.smart_test_analyze_service import SmartTestsAnalyzeService
from app.steps.smartAnalyzeDev.interfaces.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class AnalyzeFlowsStep(SmartAnalyzeDevStepInterface):
    def __init__(self):
        self.service = SmartTestsAnalyzeService()

    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        app_main_logger.debug(f"AnalyzeFlowsStep.execute(): parameters={parameters}")

        if parameters is None or parameters.groups_data is None:
            app_main_logger.warning("AnalyzeFlowsStep.execute(): parameters or groups_data is None")
            return

        self.service.analyze_flows(parameters.services_map,
                                   [],
                                   parameters.groups_data)
