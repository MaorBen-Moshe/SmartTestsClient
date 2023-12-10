from __future__ import annotations

from app.exceptions.excpetions import BadRequest
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.service_data import ServiceData
from app.steps.smartAnalyzeDev.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class SmartAnalyzeDevValidateInputStep(SmartAnalyzeDevStepInterface):

    def execute(self, parameters: AnalyzeDevAppServiceParameters):
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

                if "name" not in service:
                    raise BadRequest("Service is missing mandatory field: 'name'.")

                if "from" not in service:
                    raise BadRequest("Service is missing mandatory field: 'from'.")

                services[service.get("name")] = (ServiceData.create()
                                                 .from_version(service.get("from"))
                                                 .to_version(service.get("to"))
                                                 .build())

        parameters.data_manager.services_map = services
