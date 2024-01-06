from __future__ import annotations

from app.models.builder import Builder
from app.models.serializable_model import Serializable
from app.utils.utils import Utils


class GroupData(Serializable):

    __slots__ = [
        "_test_xml_name",
        "_test_xml_path",
        "_total_flows_count",
        "_curr_flows_count",
        "_flows"
    ]

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
        Utils.add_flows_without_duplications(self.flows, curr_flows)
        self.curr_flows_count = len(self.flows)

    @staticmethod
    def create():
        return GroupDataBuilder()


class GroupDataBuilder(Builder[GroupData]):
    def __init__(self, group_data=None):
        group_data = group_data if group_data is not None else GroupData()
        super().__init__(group_data)

    def test_xml_name(self, test_xml_name: str | None) -> GroupDataBuilder:
        self._item.test_xml_name = test_xml_name
        return self

    def test_xml_path(self, test_xml_path: str | None) -> GroupDataBuilder:
        self._item.test_xml_path = test_xml_path
        return self

    def total_flows_count(self, total_flows_count: int) -> GroupDataBuilder:
        self._item.total_flows_count = total_flows_count
        return self

    def flows(self, flows: list[str] | None) -> GroupDataBuilder:
        self._item.flows = flows
        self._item.curr_flows_count = len(flows) if flows is not None else 0
        return self
