from __future__ import annotations

from app import config, socket_handler, app_main_logger
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.steps.smartAnalyze.smart_analyze_validate_input import SmartAnalyzeValidateInputStep
from app.steps.smartAnalyze.smart_analyze_handle_groups_data_step import InitGroupsDataStep, AnalyzeFlowsStep
from app.steps.smartAnalyze.smart_analyze_html_parser_step import HtmlParserStep
from app.steps.smartAnalyze.smart_analyze_init_services_data_step import InitServiceMapStep
from app.steps.smartAnalyze.smart_analyze_prepare_response_step import PrepareResponseStep


class AnalyzeAppService:
    def __init__(self, parameters: AnalyzeAppServiceParameters):
        self.parameters = parameters
        self.parameters.data_manager.curr_group = parameters.group_name
        self.validate_input_step = SmartAnalyzeValidateInputStep()
        self.init_services_map_step = InitServiceMapStep(config.get_index_data_repository())
        self.init_groups_data_step = InitGroupsDataStep()
        self.analyze_flows_step = AnalyzeFlowsStep()
        self.html_parser = HtmlParserStep()
        self.prepare_response_step = PrepareResponseStep()

    def analyze(self) -> SmartAnalyzeResponse | None:
        # check input
        app_main_logger.info("AnalyzeAppService.analyze(): Processing payload data.")
        socket_handler.send_message("[INFO] Processing payload data.", self.parameters.session_id)
        self.validate_input_step.execute(self.parameters)

        # load version from nexus
        app_main_logger.info("AnalyzeAppService.analyze(): Loading services version from nexus.")
        socket_handler.send_message("[INFO] Loading services version from nexus.", self.parameters.session_id)
        self.init_services_map_step.execute(self.parameters)

        # load build report data
        app_main_logger.info("AnalyzeAppService.analyze(): Loading build report data.")
        socket_handler.send_message("[INFO] Loading build report data.", self.parameters.session_id)
        self.html_parser.execute(self.parameters)

        # update data per group
        app_main_logger.info("AnalyzeAppService.analyze(): Updating data per group.")
        socket_handler.send_message("[INFO] Updating data per group.", self.parameters.session_id)
        self.init_groups_data_step.execute(self.parameters)

        # analyze flows to run
        app_main_logger.info("AnalyzeAppService.analyze(): Analyzing flows to run.")
        socket_handler.send_message("[INFO] Analyzing flows to run.", self.parameters.session_id)
        self.analyze_flows_step.execute(self.parameters)

        # prepare response
        app_main_logger.info("AnalyzeAppService.analyze(): Preparing response.")
        socket_handler.send_message("[INFO] Preparing response.", self.parameters.session_id)
        self.prepare_response_step.execute(self.parameters)
        return self.parameters.smart_app_service_response
