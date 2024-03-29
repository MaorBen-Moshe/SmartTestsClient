from __future__ import annotations

from app.decorators.decorators import log_around
from app.exceptions.excpetions import BadRequest
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class SmartAnalyzeValidateInputStep(SmartAnalyzeStepInterface):
    """A class that implements the smart analyze step interface for validating the input parameters."""

    @log_around(print_output=False)
    def execute(self, parameters: AnalyzeAppServiceParameters):
        """Executes the validation step for the given parameters.

        Args:
            parameters (AnalyzeAppServiceParameters): The parameters to validate.

        Raises:
            BadRequest: If the parameters are None or missing mandatory fields: build url and valid group name.
        """
        if parameters is None:
            raise BadRequest("No payload provided.")

        if parameters.build_url is None or parameters.build_url == "":
            raise BadRequest("No build url provided.")
        if not parameters.supported_groups.contains_key(parameters.group_name):
            raise BadRequest(f"Group Name: '{parameters.group_name}' is not supported.")
