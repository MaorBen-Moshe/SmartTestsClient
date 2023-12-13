from app import app_main_logger
from app.models.group_data import GroupData
from app.models.services_data import ServicesData
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.services.interfaces.smart_prepare_response_interface import IPrepareResponseStrategy


class DebugPrepareResponseStrategy(IPrepareResponseStrategy):
    def get(self, groups_data: dict[str, GroupData], services_data: ServicesData) -> SmartAnalyzeResponse:
        app_main_logger.debug("InfoPrepareResponseStrategy.get(): Preparing response.")

        if groups_data is None or len(groups_data) == 0:
            app_main_logger.warning("PrepareResponseStep.execute(): No groups data to prepare response.")
            return SmartAnalyzeResponse.create().build()

        total_count = sum([groups_data[key].total_flows_count for key in groups_data
                           if groups_data[key].total_flows_count > 0])

        curr_flows_count = sum([groups_data[key].curr_flows_count for key in groups_data
                                if groups_data[key].curr_flows_count > 0])

        smart_app_service_response = (SmartAnalyzeResponse.create()
                                      .total_flows_count(total_count)
                                      .curr_flows_count(curr_flows_count)
                                      .groups({key:
                                               groups_data.get(key).serialize()
                                               for key in groups_data
                                               })
                                      .services({key:
                                                 services_data.get_service(key).serialize()
                                                 for key in services_data
                                                 })
                                      .build())

        app_main_logger.debug(f"InfoPrepareResponseStrategy.get(): "
                              f"response={smart_app_service_response}")

        return smart_app_service_response
