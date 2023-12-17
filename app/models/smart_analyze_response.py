from __future__ import annotations

from typing import Any

from app.models.builder import Builder
from app.models.dto.service_data_dto import ServiceDataDTO
from app.models.serializable_model import Serializable
from app.models.services_data import ServicesData


class SmartAnalyzeResponse(Serializable):
    def __init__(self):
        self.total_flows_count = 0
        self.curr_flows_count = 0
        self.groups = {}
        self.services: list[ServiceDataDTO] | None = []

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

    @property
    def services(self) -> list[ServiceDataDTO] | None:
        return self._services

    @services.setter
    def services(self, services: list[ServiceDataDTO] | None):
        self._services = services

    @staticmethod
    def create():
        return SmartAnalyzeResponseBuilder()


class SmartAnalyzeResponseBuilder(Builder[SmartAnalyzeResponse]):
    def __init__(self, smart_analyze_response=None):
        smart_analyze_response = smart_analyze_response if smart_analyze_response is not None \
                                                        else SmartAnalyzeResponse()
        super().__init__(smart_analyze_response)

    def total_flows_count(self, total_flows_count: int) -> SmartAnalyzeResponseBuilder:
        self._item.total_flows_count = total_flows_count
        return self

    def curr_flows_count(self, curr_flows_count: int) -> SmartAnalyzeResponseBuilder:
        self._item.curr_flows_count = curr_flows_count
        return self

    def groups(self, groups: dict[str, Any] | None) -> SmartAnalyzeResponseBuilder:
        self._item.groups = groups
        return self

    def services(self, services: list[ServiceDataDTO] | None) -> SmartAnalyzeResponseBuilder:
        self._item.services = services
        return self
