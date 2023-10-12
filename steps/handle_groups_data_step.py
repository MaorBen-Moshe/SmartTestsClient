from __future__ import annotations

from services.smart_test_analyze_service import SmartTestsAnalyzeService
from models.group_data import GroupData
from models.service_data import ServiceData


class HandleGroupsDataStep:
    def __init__(self, group_filter: list[str] | None):
        self.client = SmartTestsAnalyzeService()
        self.group_filter = group_filter

    def init_groups_data(self) -> dict[str, GroupData]:
        return self.client.get_all_flows_by_filter(self.group_filter)

    def analyze_flows_per_group(self,
                                services_map: dict[str, ServiceData] | None,
                                groups_data: dict[str, GroupData] | None):
        if services_map is None or groups_data is None:
            return

        self.client.analyze_flows(services_map, self.group_filter, groups_data)
