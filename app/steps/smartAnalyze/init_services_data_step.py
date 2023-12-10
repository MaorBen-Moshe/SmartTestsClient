from __future__ import annotations

from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.services.nexus_search_service import NexusSearchService
from app.steps.smartAnalyze.smart_analyze_step_interface import SmartAnalyzeStepInterface


class InitServiceMapStep(SmartAnalyzeStepInterface):

    def __init__(self, repository: str | None):
        self.nexus_search_service = NexusSearchService()
        self.repository = repository

    def execute(self, parameters: AnalyzeAppServiceParameters):
        if parameters is None or parameters.filtered_ms_list is None:
            return

        services_map = self.nexus_search_service.get_services_master_version(self.repository,
                                                                             parameters.filtered_ms_list)

        parameters.data_manager.services_map = services_map

