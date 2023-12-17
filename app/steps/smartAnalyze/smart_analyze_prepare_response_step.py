from app.decorators.decorators import log_around
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.services.smart_prepare_response_strategy_factory import PrepareResponseStrategyFactory
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class PrepareResponseStep(SmartAnalyzeStepInterface):
    def __init__(self):
        self.prepare_response_strategy_factory = PrepareResponseStrategyFactory()

    @log_around(print_output=False)
    def execute(self, parameters: AnalyzeAppServiceParameters):
        if parameters is None:
            parameters.smart_app_service_response = SmartAnalyzeResponse.create().build()
            return

        prepare_response_strategy = self.prepare_response_strategy_factory.get(parameters.res_info_level)

        parameters.smart_app_service_response = prepare_response_strategy.get(parameters.groups_data,
                                                                              parameters.services_map)
