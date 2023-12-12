from app import app_main_logger
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class PrepareResponseStep(SmartAnalyzeStepInterface):
    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        app_main_logger.debug("PrepareResponseStep.execute(): started.")
        if parameters is None:
            return

        groups_data = parameters.data_manager.groups_data if parameters.data_manager.groups_data else {}
        service_data = parameters.data_manager.services_map if parameters.data_manager.services_map else {}
        if groups_data is None or len(groups_data) == 0:
            app_main_logger.warning("PrepareResponseStep.execute(): No groups data to prepare response.")
            parameters.smart_analyze_dev_app_service_response = SmartAnalyzeResponse.create().build()
            return

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
                                                             .services({key:
                                                                        service_data.get(key).serialize()
                                                                        for key in service_data
                                                                        })
                                                             .build())

        app_main_logger.debug(f"PrepareResponseStep.execute():"
                              f" response={parameters.smart_analyze_dev_app_service_response}")
