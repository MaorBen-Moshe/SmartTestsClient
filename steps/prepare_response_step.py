from models.group_data import GroupData
from models.smart_analyze_response import SmartAnalyzeResponse, SmartAnalyzeResponseBuilder


class PrepareResponseStep:
    @staticmethod
    def prepare_response(groups_data: dict[str, GroupData]) -> SmartAnalyzeResponse:
        total_count = sum([groups_data[key].total_flows_count for key in groups_data
                           if groups_data[key].total_flows_count > 0])

        curr_flows_count = sum([groups_data[key].curr_flows_count for key in groups_data
                                if groups_data[key].curr_flows_count > 0])

        return (SmartAnalyzeResponseBuilder().total_flows_count(total_count)
                .curr_flows_count(curr_flows_count)
                .groups({key: groups_data.get(key).serialize() for key in groups_data}).build())
