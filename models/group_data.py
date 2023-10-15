from __future__ import annotations

from typing import Any


class GroupData:
    def __init__(self):
        self.group_name: str | None = None
        self.group_path: str | None = None
        self.total_flows_count: int = 0
        self.curr_flows_count: int = 0
        self.flows: list[str] | None = []

    def add_flows(self, curr_flows: list[str] | None):
        if curr_flows is None:
            return

        filtered_flows = [curr_flow for curr_flow in curr_flows if curr_flow not in self.flows]
        self.flows.extend(filtered_flows)
        self.curr_flows_count += len(filtered_flows)

    def serialize(self) -> dict[str, Any]:
        return self.__dict__


class GroupDataBuilder:
    def __init__(self):
        self.group_data = GroupData()

    def build(self) -> GroupData:
        return self.group_data

    def group_name(self, group_name: str | None) -> GroupDataBuilder:
        self.group_data.group_name = group_name
        return self

    def group_path(self, group_path: str | None) -> GroupDataBuilder:
        self.group_data.group_path = group_path
        return self

    def total_flows_count(self, total_flows_count: int) -> GroupDataBuilder:
        self.group_data.total_flows_count = total_flows_count
        return self

    def flows(self, flows: list[str] | None) -> GroupDataBuilder:
        self.group_data.flows = flows
        self.group_data.curr_flows_count = len(flows) if flows is not None else 0
        return self
