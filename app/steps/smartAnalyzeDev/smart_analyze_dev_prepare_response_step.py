from app import app_main_logger
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.services.smart_prepare_response_strategy_factory import PrepareResponseStrategyFactory
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class PrepareResponseStep(SmartAnalyzeStepInterface):
    def __init__(self):
        self.prepare_response_strategy_factory = PrepareResponseStrategyFactory()

    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        app_main_logger.debug("PrepareResponseStep.execute(): started.")
        if parameters is None:
            parameters.smart_analyze_dev_app_service_response = SmartAnalyzeResponse.create().build()
            return

        prepare_response_strategy = self.prepare_response_strategy_factory.get(parameters.res_info_level)

        parameters.smart_analyze_dev_app_service_response = prepare_response_strategy.get(
            parameters.groups_data,
            parameters.services_map)

        app_main_logger.debug(f"PrepareResponseStep.execute():"
                              f" response={parameters.smart_analyze_dev_app_service_response}")
