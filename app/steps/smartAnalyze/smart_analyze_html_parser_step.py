from __future__ import annotations

from app import app_main_logger
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.services.html_parser_service import HtmlParserService
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class HtmlParserStep(SmartAnalyzeStepInterface):
    def __init__(self):
        self.html_parser_service = HtmlParserService()

    def execute(self, parameters: AnalyzeAppServiceParameters):
        app_main_logger.debug(f"HtmlParserStep.execute(): Loading build report data. build_url={parameters.build_url}")

        if parameters is None or parameters.build_url is None or parameters.data_manager is None:
            return

        self.html_parser_service.load_html(parameters.build_url,
                                           parameters.data_manager.services_map,
                                           parameters.curr_group_data.filtered_ms_list)

        app_main_logger.debug(f"HtmlParserStep.execute(): Loading build report data completed.")
