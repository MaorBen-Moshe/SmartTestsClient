from __future__ import annotations

from app.models.serializable_model import Serializable


class GroupDataDTO(Serializable):
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
