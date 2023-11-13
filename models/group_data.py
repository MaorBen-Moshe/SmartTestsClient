from __future__ import annotations

from typing import Any

from utils import utils


class GroupData:
    def __init__(self):
        self.test_xml_name = None
        self.test_xml_path = None
        self.total_flows_count = 0
        self.curr_flows_count = 0
        self.flows = []

    @property
    def test_xml_name(self) -> str | None:
        return self._test_xml_name

    @test_xml_name.setter
    def test_xml_name(self, test_xml_name: str | None):
        self._test_xml_name = test_xml_name

    @property
    def test_xml_path(self) -> str | None:
        return self._test_xml_path

    @test_xml_path.setter
    def test_xml_path(self, test_xml_path: str | None):
        self._test_xml_path = test_xml_path

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
        return utils.Utils.serialize_class(self, [])


class GroupDataBuilder:
    def __init__(self):
        self.group_data = GroupData()

    def build(self) -> GroupData:
        return self.group_data

    def test_xml_name(self, test_xml_name: str | None) -> GroupDataBuilder:
        self.group_data.test_xml_name = test_xml_name
        return self

    def test_xml_path(self, test_xml_path: str | None) -> GroupDataBuilder:
        self.group_data.test_xml_path = test_xml_path
        return self

    def total_flows_count(self, total_flows_count: int) -> GroupDataBuilder:
        self.group_data.total_flows_count = total_flows_count
        return self

    def flows(self, flows: list[str] | None) -> GroupDataBuilder:
        self.group_data.flows = flows
        self.group_data.curr_flows_count = len(flows) if flows is not None else 0
        return self
