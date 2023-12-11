from app import app_main_logger
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.steps.smartAnalyze.interfaces.smart_analyze_step_interface import SmartAnalyzeStepInterface


class PrepareResponseStep(SmartAnalyzeStepInterface):
    def execute(self, parameters: AnalyzeAppServiceParameters):
        app_main_logger.debug("PrepareResponseStep.execute(): Preparing response.")

        if parameters is None:
            return

        groups_data = parameters.data_manager.groups_data if parameters.data_manager.groups_data else {}
        service_data = parameters.data_manager.services_map if parameters.data_manager.services_map else {}
        if groups_data is None or len(groups_data) == 0:
            app_main_logger.warning("PrepareResponseStep.execute(): No groups data to prepare response.")
            parameters.smart_app_service_response = SmartAnalyzeResponse.create().build()
            return

        total_count = sum([groups_data[key].total_flows_count for key in groups_data
                           if groups_data[key].total_flows_count > 0])

        flows_set = set()
        for key in groups_data:
            if groups_data[key].curr_flows_count > 0:
                flows_set.update(groups_data[key].flows if groups_data[key].flows else [])

        parameters.smart_app_service_response = (SmartAnalyzeResponse.create()
                                                 .total_flows_count(total_count)
                                                 .curr_flows_count(len(flows_set))
                                                 .groups({key:
                                                          groups_data.get(key).serialize()
                                                          for key in groups_data
                                                          })
                                                 .services({key:
                                                            service_data.get(key).serialize()
                                                            for key in service_data
                                                            })
                                                 .build())

        app_main_logger.debug(f"PrepareResponseStep.execute(): response={parameters.smart_app_service_response}")
