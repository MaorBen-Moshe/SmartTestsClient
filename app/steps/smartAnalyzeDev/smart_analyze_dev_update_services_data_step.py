from app import app_main_logger
from app.decorators.decorators import log_around
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.services.smart_analyze_dev_update_services_data_service import UpdateServiceDataService
from app.steps.smartAnalyzeDev.interfaces.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class UpdateServiceDataStep(SmartAnalyzeDevStepInterface):
    def __init__(self, repository):
        super().__init__()
        self.update_services_data_service = UpdateServiceDataService()
        self.repository = repository

    @log_around(print_output=False)
    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        if (parameters is None or
                parameters.services_map is None or
                len(parameters.services_map) == 0):
            app_main_logger.warning("UpdateServiceDataStep.execute(): No services data to update.")
            return

        updated_services_data = self.update_services_data_service.update_services_data(self.repository,
                                                                                       parameters.services_map)

        parameters.services_map.merge(updated_services_data)
