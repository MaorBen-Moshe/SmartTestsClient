from __future__ import annotations

from app import app_main_logger, config
from app.constants.constants import SERVICE_FROM_KEY
from app.decorators.decorators import log_around
from app.exceptions.excpetions import BadRequest
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.steps.smartAnalyzeDev.interfaces.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class SmartAnalyzeDevValidateInputStep(SmartAnalyzeDevStepInterface):

    @log_around(print_output=False)
    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        if parameters is None:
            raise BadRequest("No payload provided.")

        supported_services = config.get_supported_services()
        if parameters.services_map and len(parameters.services_map) > 0:
            for service_name in parameters.services_map:
                service = parameters.services_map.get_item(service_name)
                supported_service_template = supported_services.get_item(service_name)
                if service.from_version is None:
                    if service.pull_request_id is None:
                        raise BadRequest(f"Service '{service_name}' is missing mandatory field: "
                                         f"'{SERVICE_FROM_KEY}'.")
                    else:
                        app_main_logger.warning("Provided from version and pull request id. "
                                                "Ignoring 'from' version data.")

                service.from_version = None if service.pull_request_id else service.from_version
                service.to_version = None if service.pull_request_id else service.to_version

                if supported_service_template is not None:
                    service.repo_name = supported_service_template.repo_name
                    service.project = supported_service_template.project
                    service.related_group = supported_service_template.related_group
        else:
            app_main_logger.warning("SmartAnalyzeDevValidateInputStep.execute(): No services provided.")

        app_main_logger.debug(f"SmartAnalyzeDevValidateInputStep.execute(): services: {parameters.services_map}")
