from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.services.smart_analyze_dev_update_services_data_service import UpdateServiceDataService
from app.steps.smartAnalyzeDev.smart_analyze_dev_step_interface import SmartAnalyzeDevStepInterface


class UpdateServiceDataStep(SmartAnalyzeDevStepInterface):
    def __init__(self, repository):
        super().__init__()
        self.update_services_data_service = UpdateServiceDataService()
        self.repository = repository

    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        if (parameters is None or
                parameters.data_manager is None or
                parameters.data_manager.services_map is None or
                len(parameters.data_manager.services_map) == 0):
            return

        updated_services_data = self.update_services_data_service.update_services_data(self.repository,
                                                                                       parameters.data_manager.services_map)

        parameters.data_manager.services_map = updated_services_data
