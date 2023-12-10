from __future__ import annotations

from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app import config, socket_handler
from app.models.data_manager import DataManager
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.steps.check_analyze_input import CheckAnalyzeClientInputStep
from app.steps.handle_groups_data_step import HandleGroupsDataStep
from app.steps.html_parser_step import HtmlParserStep
from app.steps.init_services_data_step import InitServiceMapStep
from app.steps.prepare_response_step import PrepareResponseStep


class AnalyzeAppService:
    def __init__(self, parameters: AnalyzeAppServiceParameters):
        self.parameters = parameters
        self.config_manager = config
        self.data_manager = DataManager()
        self.data_manager.curr_group = parameters.group_name
        self.handle_group_data_step = HandleGroupsDataStep()
        self.html_parser = HtmlParserStep()
        self.prepare_response_step = PrepareResponseStep()

    def analyze(self) -> SmartAnalyzeResponse:
        # check input
        socket_handler.send_message("[INFO] Processing payload data.", self.parameters.session_id)
        CheckAnalyzeClientInputStep.check_input(self.parameters, self.parameters.supported_groups)

        # load version from nexus
        socket_handler.send_message("[INFO] Loading services version from nexus.", self.parameters.session_id)
        repository = self.config_manager.get_index_data_repository()
        self.data_manager.services_map = InitServiceMapStep.init_services_map(repository,
                                                                              self.parameters.filtered_ms_list)

        # load build report data
        socket_handler.send_message("[INFO] Loading build report data.", self.parameters.session_id)
        self.html_parser.load_html_step(self.parameters.build_url,
                                        self.data_manager.services_map,
                                        self.parameters.filtered_ms_list)

        # update data per group
        socket_handler.send_message("[INFO] Updating data per group.", self.parameters.session_id)
        self.data_manager.groups_data = self.handle_group_data_step.init_groups_data(self.data_manager.filter_for_curr_group)

        # analyze flows to run
        socket_handler.send_message("[INFO] Analyzing flows to run.", self.parameters.session_id)
        self.handle_group_data_step.analyze_flows_per_group(self.data_manager.services_map,
                                                            self.data_manager.groups_data,
                                                            self.data_manager.filter_for_curr_group)

        # prepare response
        socket_handler.send_message("[INFO] Preparing response.", self.parameters.session_id)

        return self.prepare_response_step.prepare_response(self.data_manager.groups_data)
