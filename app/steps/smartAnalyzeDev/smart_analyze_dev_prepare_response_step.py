from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.steps.smartAnalyze.smart_analyze_step_interface import SmartAnalyzeStepInterface


class PrepareResponseStep(SmartAnalyzeStepInterface):
    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        if parameters is None:
            return

        groups_data = parameters.data_manager.groups_data
        if groups_data is None or len(groups_data) == 0:
            return

        total_count = sum([groups_data[key].total_flows_count for key in groups_data
                           if groups_data[key].total_flows_count > 0])

        flows_set = set()
        for key in groups_data:
            if groups_data[key].curr_flows_count > 0:
                flows_set.update(groups_data[key].flows if groups_data[key].flows else [])

        parameters.smart_analyze_dev_app_service_response = (SmartAnalyzeResponse.create()
                                                             .total_flows_count(total_count)
                                                             .curr_flows_count(len(flows_set))
                                                             .groups({key:
                                                                      groups_data.get(key).serialize()
                                                                      for key in groups_data
                                                                      })
                                                             .build())
