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
                parameters.curr_group_data.services_data is None):
            return

        ms_list = (parameters.curr_group_data.services_data.get_item(service) for
                   service in parameters.curr_group_data.services_data)

        res = self.nexus_search_service.get_services_master_version(self.repository, ms_list)

        parameters.services_map.merge(res)

        app_main_logger.debug(f"InitServiceMapStep.execute() services_map={parameters.services_map}")
