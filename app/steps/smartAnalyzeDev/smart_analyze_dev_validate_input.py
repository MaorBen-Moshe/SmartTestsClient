from __future__ import annotations

from app import app_main_logger
from app.constants.constants import SERVICE_FROM_KEY, PULL_REQUEST_ID_KEY
from app.decorators.decorators import log_around
from app.exceptions.excpetions import BadRequest
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.steps.smartAnalyzeDev.interfaces.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class SmartAnalyzeDevValidateInputStep(SmartAnalyzeDevStepInterface):
    """A class that implements the smart analyze dev step interface for validating the input parameters."""

    @log_around(print_output=False)
    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        """Executes the validation step for the given parameters.

        Args:
            parameters (AnalyzeDevAppServiceParameters): The parameters to validate.

        Raises:
            BadRequest: If the parameters are None or invalid.
        """
        if parameters is None:
            raise BadRequest("No payload provided.")

        if parameters.services_map and len(parameters.services_map) > 0:
            for service_name in parameters.services_map:
                service = parameters.services_map.get_item(service_name)
                if service.from_version is None:
                    if service.pull_request_id is None:
                        raise BadRequest(f"Service '{service_name}' is missing mandatory field: "
                                         f"'{SERVICE_FROM_KEY}' or '{PULL_REQUEST_ID_KEY}'.")
                    else:
                        service.to_version = None
                else:
                    if service.pull_request_id is not None:
                        app_main_logger.warning("Provided from version and pull request id. "
                                                "Ignoring 'from' version data.")
                        service.from_version = None
                        service.to_version = None

        else:
            app_main_logger.warning("SmartAnalyzeDevValidateInputStep.execute(): No services provided.")

        app_main_logger.debug(f"SmartAnalyzeDevValidateInputStep.execute(): services: {parameters.services_map}")
