from __future__ import annotations


class GroupData:
    def __init__(self):
        self.group_name = None
        self.group_path = None
        self.total_flows_count = 0
        self.curr_flows_count = 0
        self.flows = []

    def add_flows(self, curr_flows: list[str]):
        filtered_flows = [curr_flow for curr_flow in curr_flows if curr_flow not in self.flows]
        self.flows.extend(filtered_flows)
        self.curr_flows_count += len(filtered_flows)


class GroupDataBuilder:
    def __init__(self):
        self.group_data = GroupData()

    def build(self) -> GroupData:
        return self.group_data

    def group_name(self, group_name: str) -> GroupDataBuilder:
        self.group_data.group_name = group_name
        return self

    def group_path(self, group_path: str) -> GroupDataBuilder:
        self.group_data.group_path = group_path
        return self

    def total_flows_count(self, total_flows_count: int) -> GroupDataBuilder:
        self.group_data.total_flows_count = total_flows_count
        return self

    def flows(self, flows: list[str]) -> GroupDataBuilder:
        self.group_data.flows = flows
        self.group_data.curr_flows_count = len(flows)
        return self
