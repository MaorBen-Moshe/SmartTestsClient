from __future__ import annotations

from typing import Any

from app.models.builder import Builder
from app.utils import utils


class SmartAnalyzeResponse:
    def __init__(self):
        self.total_flows_count = 0
        self.curr_flows_count = 0
        self.groups = None

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
    def groups(self) -> dict[str, Any] | None:
        return self._groups

    @groups.setter
    def groups(self, groups: dict[str, Any] | None):
        self._groups = groups

    def serialize(self) -> dict[str, Any]:
        return utils.Utils.serialize_class(self, [])

    @staticmethod
    def create():
        return SmartAnalyzeResponseBuilder()


class SmartAnalyzeResponseBuilder(Builder[SmartAnalyzeResponse]):
    def __init__(self, smart_analyze_response=None):
        smart_analyze_response = smart_analyze_response if smart_analyze_response is not None else SmartAnalyzeResponse()
        super().__init__(smart_analyze_response)

    def total_flows_count(self, total_flows_count: int) -> SmartAnalyzeResponseBuilder:
        self.item.total_flows_count = total_flows_count
        return self

    def curr_flows_count(self, curr_flows_count: int) -> SmartAnalyzeResponseBuilder:
        self.item.curr_flows_count = curr_flows_count
        return self

    def groups(self, groups: dict[str, Any] | None) -> SmartAnalyzeResponseBuilder:
        self.item.groups = groups
        return self
