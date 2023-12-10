from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.steps.smartAnalyze.smart_analyze_step_interface import SmartAnalyzeStepInterface


class PrepareResponseStep(SmartAnalyzeStepInterface):
    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        if parameters is None:
            return

        groups_data = parameters.data_manager.groups_data

        total_count = sum([groups_data[key].total_flows_count for key in groups_data
                           if groups_data[key].total_flows_count > 0])

        curr_flows_count = sum([groups_data[key].curr_flows_count for key in groups_data
                                if groups_data[key].curr_flows_count > 0])

        parameters.smart_analyze_dev_app_service_response = (SmartAnalyzeResponse.create()
                                                             .total_flows_count(total_count)
                                                             .curr_flows_count(curr_flows_count)
                                                             .groups({key:
                                                                          groups_data.get(key).serialize()
                                                                      for key in groups_data
                                                                      })
                                                             .build())
