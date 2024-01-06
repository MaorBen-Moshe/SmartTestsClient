from __future__ import annotations

from app import app_main_logger
from app.decorators.decorators import log_around
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.services.smart_test_analyze_service import SmartTestsAnalyzeService
from app.steps.smartAnalyzeDev.interfaces.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class InitGroupsDataStep(SmartAnalyzeDevStepInterface):
    def __init__(self):
        self.service = SmartTestsAnalyzeService()

    @log_around(print_output=False)
    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        if parameters is None:
            return

        groups_data = self.service.get_all_flows_by_filter()

        parameters.groups_data.merge(groups_data)

        app_main_logger.debug(f"InitGroupsDataStep.execute(): groups_data_after_merge={parameters.groups_data}")
