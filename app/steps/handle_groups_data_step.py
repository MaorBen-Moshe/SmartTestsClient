from __future__ import annotations

from app.services.smart_test_analyze_service import SmartTestsAnalyzeService
from app.models.group_data import GroupData
from app.models.service_data import ServiceData


class HandleGroupsDataStep:
    def __init__(self):
        self.client = SmartTestsAnalyzeService()

    def init_groups_data(self, group_filter: list[str] | None) -> dict[str, GroupData]:
        return self.client.get_all_flows_by_filter(group_filter)

    def analyze_flows_per_group(self,
                                services_map: dict[str, ServiceData] | None,
                                groups_data: dict[str, GroupData] | None,
                                group_filter: list[str] | None):
        if services_map is None or groups_data is None:
            return

        self.client.analyze_flows(services_map, group_filter, groups_data)
