from __future__ import annotations

from app.exceptions.excpetions import BadRequest
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.steps.smartAnalyze.smart_analyze_step_interface import SmartAnalyzeStepInterface


class CheckAnalyzeClientInputStep(SmartAnalyzeStepInterface):

    def execute(self, parameters: AnalyzeAppServiceParameters):
        if parameters is None:
            raise BadRequest("No payload provided.")

        if parameters.build_url is None or parameters.build_url == "":
            raise BadRequest("No build url provided.")
        if parameters.group_name not in parameters.supported_groups:
            raise BadRequest(f"Group Name: '{parameters.group_name}' is not supported.")
