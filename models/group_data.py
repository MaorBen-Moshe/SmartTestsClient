from __future__ import annotations


class GroupData:
    def __init__(self):
        self.group_name = None
        self.group_path = None
        self.total_flows_count = 0
        self.curr_flows_count = 0
        self.flows = []


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

    def curr_flows_count(self, curr_flows_count: int) -> GroupDataBuilder:
        self.group_data.curr_flows_count = curr_flows_count
        return self

    def flows(self, flows: list[str]) -> GroupDataBuilder:
        self.group_data.flows = flows
        return self
