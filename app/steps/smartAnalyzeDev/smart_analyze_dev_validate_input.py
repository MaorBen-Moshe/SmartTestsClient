from __future__ import annotations

from app import app_main_logger
from app.constants.constants import SERVICE_NAME_KEY, SERVICE_FROM_KEY, SERVICE_TO_KEY
from app.exceptions.excpetions import BadRequest
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.service_data import ServiceData
from app.steps.smartAnalyzeDev.interfaces.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class SmartAnalyzeDevValidateInputStep(SmartAnalyzeDevStepInterface):

    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        app_main_logger.debug("SmartAnalyzeDevValidateInputStep.execute(): validating input.")

        if parameters is None:
            raise BadRequest("No payload provided.")

        if parameters.services_input is None:
            raise BadRequest("No services input provided.")

        if type(parameters.services_input) != list:
            raise BadRequest("Services input should be a list.")

        services: dict[str, ServiceData] = {}
        if len(parameters.services_input) > 0:
            for service in parameters.services_input:
                if type(service) != dict:
                    raise BadRequest("Each Service in services should be a dictionary.")

                if SERVICE_NAME_KEY not in service:
                    raise BadRequest(f"Service is missing mandatory field: '{SERVICE_NAME_KEY}'.")

                if SERVICE_FROM_KEY not in service:
                    raise BadRequest(f"Service '{service.get(SERVICE_NAME_KEY)}' is missing mandatory field: "
                                     f"'{SERVICE_FROM_KEY}'.")

                services[service.get(SERVICE_NAME_KEY)] = (ServiceData.create()
                                                 .from_version(service.get(SERVICE_FROM_KEY))
                                                 .to_version(service.get(SERVICE_TO_KEY, None))
                                                 .build())
        else:
            app_main_logger.warning("SmartAnalyzeDevValidateInputStep.execute(): No services provided.")

        app_main_logger.debug(f"SmartAnalyzeDevValidateInputStep.execute(): services: {services}")

        parameters.data_manager.services_map = services
