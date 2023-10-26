from __future__ import annotations

from typing import Any

from utils import utils


class GroupData:
    def __init__(self):
        self.group_name = None
        self.group_path = None
        self.total_flows_count = 0
        self.curr_flows_count = 0
        self.flows = []

    @property
    def group_name(self) -> str | None:
        return self._group_name

    @group_name.setter
    def group_name(self, group_name: str | None):
        self._group_name = group_name

    @property
    def group_path(self) -> str | None:
        return self._group_path

    @group_path.setter
    def group_path(self, group_path: str | None):
        self._group_path = group_path

    @property
    def total_flows_count(self) -> int:
        return self._total_flows_count

    @total_flows_count.setter
    def total_flows_count(self, total_flows_count: int):
        self._total_flows_count = total_flows_count

    @property
    def curr_flows_count(self) -> int:
        return self._curr_flows_count

    @curr_flows_count.setter
    def curr_flows_count(self, curr_flows_count: int):
        self._curr_flows_count = curr_flows_count

    @property
    def flows(self) -> list[str] | None:
        return self._flows

    @flows.setter
    def flows(self, flows: list[str] | None):
        self._flows = flows

    def add_flows(self, curr_flows: list[str] | None):
        if curr_flows is None:
            return

        filtered_flows = [curr_flow for curr_flow in curr_flows if curr_flow not in self.flows]
        self.flows.extend(filtered_flows)
        self.curr_flows_count += len(filtered_flows)

    def serialize(self) -> dict[str, Any]:
        return utils.Utils.serialize_class(self)


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
