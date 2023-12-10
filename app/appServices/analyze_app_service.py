from __future__ import annotations

from app import config, socket_handler
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.steps.smartAnalyze.check_analyze_input import CheckAnalyzeClientInputStep
from app.steps.smartAnalyze.handle_groups_data_step import InitGroupsDataStep, AnalyzeFlowsStep
from app.steps.smartAnalyze.html_parser_step import HtmlParserStep
from app.steps.smartAnalyze.init_services_data_step import InitServiceMapStep
from app.steps.smartAnalyze.prepare_response_step import PrepareResponseStep


class AnalyzeAppService:
    def __init__(self, parameters: AnalyzeAppServiceParameters):
        self.parameters = parameters
        self.config_manager = config
        self.parameters.data_manager.curr_group = parameters.group_name
        self.validate_input_step = CheckAnalyzeClientInputStep()
        self.init_services_map_step = InitServiceMapStep(self.config_manager.get_index_data_repository())
        self.init_groups_data_step = InitGroupsDataStep()
        self.analyze_flows_step = AnalyzeFlowsStep()
        self.html_parser = HtmlParserStep()
        self.prepare_response_step = PrepareResponseStep()

    def analyze(self) -> SmartAnalyzeResponse:
        # check input
        socket_handler.send_message("[INFO] Processing payload data.", self.parameters.session_id)
        self.validate_input_step.execute(self.parameters)

        # load version from nexus
        socket_handler.send_message("[INFO] Loading services version from nexus.", self.parameters.session_id)
        self.init_services_map_step.execute(self.parameters)

        # load build report data
        socket_handler.send_message("[INFO] Loading build report data.", self.parameters.session_id)
        self.html_parser.execute(self.parameters)

        # update data per group
        socket_handler.send_message("[INFO] Updating data per group.", self.parameters.session_id)
        self.init_groups_data_step.execute(self.parameters)

        # analyze flows to run
        socket_handler.send_message("[INFO] Analyzing flows to run.", self.parameters.session_id)
        self.analyze_flows_step.execute(self.parameters)

        # prepare response
        socket_handler.send_message("[INFO] Preparing response.", self.parameters.session_id)
        self.prepare_response_step.execute(self.parameters)
        return self.parameters.smart_app_service_response
