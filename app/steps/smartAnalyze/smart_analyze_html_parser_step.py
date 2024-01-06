from __future__ import annotations

from app import app_main_logger
from app.decorators.decorators import log_around
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.services.html_parser_service import HtmlParserService
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class HtmlParserStep(SmartAnalyzeStepInterface):
    def __init__(self):
        self.html_parser_service = HtmlParserService()

    @log_around(print_output=False)
    def execute(self, parameters: AnalyzeAppServiceParameters):
        if parameters is None or parameters.build_url is None:
            app_main_logger.warning("HtmlParserStep.execute(): parameters is None.")
            return

        self.html_parser_service.load_html(parameters.build_url,
                                           parameters.services_map)

        app_main_logger.debug(f"HtmlParserStep.execute(): services={parameters.services_map}")
