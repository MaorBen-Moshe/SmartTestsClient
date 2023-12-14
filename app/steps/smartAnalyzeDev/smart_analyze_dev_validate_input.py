from __future__ import annotations

from typing import Any

from app import app_main_logger
from app.constants.constants import SERVICE_NAME_KEY, SERVICE_FROM_KEY, SERVICE_TO_KEY, PULL_REQUEST_ID_KEY
from app.exceptions.excpetions import BadRequest
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.service_data import ServiceData
from app.models.supported_groups import SupportedGroups
from app.steps.smartAnalyzeDev.interfaces.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface
from app.utils.utils import Utils


class SmartAnalyzeDevValidateInputStep(SmartAnalyzeDevStepInterface):

    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        app_main_logger.debug("SmartAnalyzeDevValidateInputStep.execute(): validating input.")

        if parameters is None:
            raise BadRequest("No payload provided.")

        if parameters.services_input is None:
            raise BadRequest("No services input provided.")

        if type(parameters.services_input) != list:
            raise BadRequest("Services input should be a list.")

        if len(parameters.services_input) > 0:
            for service in parameters.services_input:
                if type(service) != dict:
                    raise BadRequest("Each Service in services should be a dictionary.")

                if SERVICE_NAME_KEY not in service:
                    raise BadRequest(f"Service is missing mandatory field: '{SERVICE_NAME_KEY}'.")

                if SERVICE_FROM_KEY not in service:
                    if service.get(PULL_REQUEST_ID_KEY) is None:
                        raise BadRequest(f"Service '{service.get(SERVICE_NAME_KEY)}' is missing mandatory field: "
                                         f"'{SERVICE_FROM_KEY}'.")
                    else:
                        app_main_logger.warning("Provided from version and pull request id. "
                                                "Ignoring 'from' version data.")

                service_name, service_data = self.__build_services_data(service, parameters.supported_groups)
                parameters.services_map.add_item(service_name, service_data)
        else:
            app_main_logger.warning("SmartAnalyzeDevValidateInputStep.execute(): No services provided.")

        app_main_logger.debug(f"SmartAnalyzeDevValidateInputStep.execute(): services: {parameters.services_map}")

    @staticmethod
    def __build_services_data(service: dict[str, Any], supported_groups: SupportedGroups) -> (str, ServiceData):
        service_name = service.get(SERVICE_NAME_KEY)
        service_data = None
        if service_name:
            pull_request_id = service.get(PULL_REQUEST_ID_KEY)
            from_version = service.get(SERVICE_FROM_KEY) if pull_request_id is None else None
            to_version = service.get(SERVICE_TO_KEY) if pull_request_id is None else None
            project = Utils.get_project_name_from_supported_group(service_name, supported_groups)
            service_data = (ServiceData.create()
                            .from_version(from_version)
                            .to_version(to_version)
                            .project(project)
                            .pull_request_id(pull_request_id)
                            .build())

        return service_name, service_data
