from app import app_main_logger
from app.decorators.decorators import log_around
from app.mappers.group_data_mapper import GroupDataMapper
from app.models.groups_data import TestGroupsData
from app.models.services_data import ServicesData
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.services.interfaces.smart_prepare_response_interface import IPrepareResponseStrategy


class InfoPrepareResponseStrategy(IPrepareResponseStrategy):

    @log_around(print_output=True)
    def get(self, groups_data: TestGroupsData, services_data: ServicesData) -> SmartAnalyzeResponse:
        if groups_data is None or len(groups_data) == 0:
            app_main_logger.warning("PrepareResponseStep.execute(): No groups data to prepare response.")
            return SmartAnalyzeResponse.create().build()

        total_count = sum([groups_data.get_item(key).total_flows_count for key in groups_data
                           if groups_data.get_item(key).total_flows_count > 0])

        curr_flows_count = sum([groups_data.get_item(key).curr_flows_count for key in groups_data
                                if groups_data.get_item(key).curr_flows_count > 0])

        smart_app_service_response = (SmartAnalyzeResponse.create()
                                      .total_flows_count(total_count)
                                      .curr_flows_count(curr_flows_count)
                                      .groups({key:
                                               GroupDataMapper.map_to_dto(groups_data.get_item(key))
                                               for key in groups_data
                                               if groups_data.get_item(key) is not None
                                               })
                                      .build())

        return smart_app_service_response
