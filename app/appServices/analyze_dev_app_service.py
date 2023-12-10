from __future__ import annotations

from app import config, socket_handler
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.steps.smartAnalyzeDev.smart_analyze_dev_analyze_flows_step import AnalyzeFlowsStep
from app.steps.smartAnalyzeDev.smart_analyze_dev_init_groups_data_step import InitGroupsDataStep
from app.steps.smartAnalyzeDev.smart_analyze_dev_prepare_response_step import PrepareResponseStep
from app.steps.smartAnalyzeDev.smart_analyze_dev_update_services_data_step import UpdateServiceDataStep
from app.steps.smartAnalyzeDev.smart_analyze_dev_validate_input import SmartAnalyzeDevValidateInputStep


class AnalyzeDevAppService:
    def __init__(self, parameters: AnalyzeDevAppServiceParameters):
        self.parameters = parameters
        self.validate_input_step = SmartAnalyzeDevValidateInputStep()
        self.update_services_data_step = UpdateServiceDataStep(config.get_index_data_repository())
        self.init_groups_data_step = InitGroupsDataStep()
        self.analyze_flows_step = AnalyzeFlowsStep()
        self.prepare_response_step = PrepareResponseStep()

    def analyze_dev(self) -> SmartAnalyzeResponse | None:
        socket_handler.send_message("[INFO] Processing payload data.", self.parameters.session_id)
        self.validate_input_step.execute(self.parameters)

        socket_handler.send_message("[INFO] Updating services data.", self.parameters.session_id)
        self.update_services_data_step.execute(self.parameters)

        socket_handler.send_message("[INFO] Initializing groups data.", self.parameters.session_id)
        self.init_groups_data_step.execute(self.parameters)

        socket_handler.send_message("[INFO] Analyzing flows.", self.parameters.session_id)
        self.analyze_flows_step.execute(self.parameters)

        socket_handler.send_message("[INFO] Preparing response.", self.parameters.session_id)
        self.prepare_response_step.execute(self.parameters)
        return self.parameters.smart_analyze_dev_app_service_response
