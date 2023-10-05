from client.smart_test_client import SmartTestsClient
from models.group_data import GroupData
from models.service_data import ServiceData


class HandleGroupsDataStep:
    def __init__(self, group_filter: list[str]):
        self.client = SmartTestsClient()
        self.group_filter = group_filter

    def init_groups_data(self) -> dict[str, GroupData]:
        return self.client.get_all_flows_by_filter(self.group_filter)

    def analyze_flows_per_group(self, services_map: dict[str, ServiceData], groups_data: dict[str, GroupData]):
        self.client.analyze_flows(services_map, self.group_filter, groups_data)
