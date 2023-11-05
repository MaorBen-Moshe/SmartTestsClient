from __future__ import annotations

from typing import Any

from utils import utils


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


class SmartAnalyzeResponseBuilder:
    def __init__(self):
        self.smart_analyze_response = SmartAnalyzeResponse()

    def build(self) -> SmartAnalyzeResponse:
        return self.smart_analyze_response

    def total_flows_count(self, total_flows_count: int) -> SmartAnalyzeResponseBuilder:
        self.smart_analyze_response.total_flows_count = total_flows_count
        return self

    def curr_flows_count(self, curr_flows_count: int) -> SmartAnalyzeResponseBuilder:
        self.smart_analyze_response.curr_flows_count = curr_flows_count
        return self

    def groups(self, groups: dict[str, Any] | None) -> SmartAnalyzeResponseBuilder:
        self.smart_analyze_response.groups = groups
        return self
