from app import app_main_logger
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.services.smart_analyze_dev_update_services_data_service import UpdateServiceDataService
from app.steps.smartAnalyzeDev.interfaces.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class UpdateServiceDataStep(SmartAnalyzeDevStepInterface):
    def __init__(self, repository):
        super().__init__()
        self.update_services_data_service = UpdateServiceDataService()
        self.repository = repository

    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        app_main_logger.debug("UpdateServiceDataStep.execute(): start")

        if (parameters is None or
                parameters.data_manager is None or
                parameters.data_manager.services_map is None or
                len(parameters.data_manager.services_map) == 0):
            app_main_logger.warning("UpdateServiceDataStep.execute(): No services data to update.")
            return

        updated_services_data = self.update_services_data_service.update_services_data(self.repository,
                                                                                       parameters.data_manager.services_map)

        app_main_logger.debug(f"UpdateServiceDataStep.execute(): services={updated_services_data}")

        parameters.data_manager.services_map = updated_services_data
