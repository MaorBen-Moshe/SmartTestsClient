from __future__ import annotations

from typing import Any


def serialize():
    return __dict__


class SmartAnalyzeResponse:
    def __init__(self):
        self.total_flows_count: int = 0
        self.curr_flows_count: int = 0
        self.groups: dict[str, Any] | None = None

    def serialize(self) -> dict[str, Any]:
        return self.__dict__


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
