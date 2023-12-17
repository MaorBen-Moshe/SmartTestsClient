from __future__ import annotations

from app import app_main_logger
from app.decorators.decorators import log_around
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.services.nexus_search_service import NexusSearchService
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class InitServiceMapStep(SmartAnalyzeStepInterface):

    def __init__(self, repository: str | None):
        self.nexus_search_service = NexusSearchService()
        self.repository = repository

    @log_around(print_output=False)
    def execute(self, parameters: AnalyzeAppServiceParameters):
        if (parameters is None
                or parameters.curr_group_data is None or
                parameters.curr_group_data.ms_list is None):
            return

        services_map = self.nexus_search_service.get_services_master_version(
            self.repository,
            parameters.curr_group_data.ms_list,
            parameters.curr_group_data.project)

        parameters.services_map.merge(services_map)

        app_main_logger.debug(f"InitServiceMapStep.execute() services_map_after_merge={parameters.services_map}")
