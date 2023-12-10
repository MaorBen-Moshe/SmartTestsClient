from __future__ import annotations

from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.services.smart_test_analyze_service import SmartTestsAnalyzeService
from app.steps.smartAnalyzeDev.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class AnalyzeFlowsStep(SmartAnalyzeDevStepInterface):
    def __init__(self):
        self.service = SmartTestsAnalyzeService()

    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        if parameters is None or parameters.data_manager.groups_data is None:
            return

        self.service.analyze_flows(parameters.data_manager.services_map,
                                   [],
                                   parameters.data_manager.groups_data)
