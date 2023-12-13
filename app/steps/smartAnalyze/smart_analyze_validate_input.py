from __future__ import annotations

from app import app_main_logger
from app.exceptions.excpetions import BadRequest
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class SmartAnalyzeValidateInputStep(SmartAnalyzeStepInterface):

    def execute(self, parameters: AnalyzeAppServiceParameters):
        app_main_logger.debug(f"SmartAnalyzeValidateInputStep.execute(): parameters={parameters}")

        if parameters is None:
            raise BadRequest("No payload provided.")

        if parameters.build_url is None or parameters.build_url == "":
            raise BadRequest("No build url provided.")
        if not parameters.supported_groups.contains_key(parameters.group_name):
            raise BadRequest(f"Group Name: '{parameters.group_name}' is not supported.")
