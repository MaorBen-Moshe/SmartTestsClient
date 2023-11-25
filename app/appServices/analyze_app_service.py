from __future__ import annotations

from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.models.config_manager import ConfigManager
from app.models.data_manager import DataManager
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.steps.handle_groups_data_step import HandleGroupsDataStep
from app.steps.html_parser_step import HtmlParserStep
from app.steps.init_services_data_step import InitServiceMapStep
from app.steps.prepare_response_step import PrepareResponseStep


class AnalyzeAppService:
    def __init__(self, parameters: AnalyzeAppServiceParameters):
        self.supported_groups = parameters.supported_groups
        self.data_manager = DataManager()
        self.data_manager.curr_group = parameters.group_name
        self.handle_group_data_step = HandleGroupsDataStep(self.data_manager.filter_for_curr_group)
        self.html_parser = HtmlParserStep(parameters.build_url)
        self.config_manager = ConfigManager()
        self.supported_groups = parameters.supported_groups
        self.filtered_ms_list = parameters.filtered_ms_list
        self.prepare_response_step = PrepareResponseStep()

    def analyze(self) -> SmartAnalyzeResponse:
        # load index yaml
        self.data_manager.services_map = InitServiceMapStep.init_services_map(self.config_manager.get_index_data_urls(),
                                                                              self.filtered_ms_list)

        # load build report data
        self.html_parser.load_html_step(self.data_manager.services_map, self.filtered_ms_list)

        # update data per group
        self.data_manager.groups_data = self.handle_group_data_step.init_groups_data()

        # analyze flows to run
        self.handle_group_data_step.analyze_flows_per_group(self.data_manager.services_map,
                                                            self.data_manager.groups_data)

        # prepare response
        return self.prepare_response_step.prepare_response(self.data_manager.groups_data)
