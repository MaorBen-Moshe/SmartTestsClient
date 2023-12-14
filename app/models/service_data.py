from __future__ import annotations

from typing import Any

from app.models.builder import Builder
from app.utils.utils import Utils


class ServiceData:
    def __init__(self):
        self.from_version: str | None = None
        self.to_version: str | None = None
        self.flows = []
        self.project: str | None = None
        self.pull_request_id: str | None = None

    @property
    def from_version(self) -> str | None:
        return self._from_version

    @from_version.setter
    def from_version(self, from_version: str | None) -> None:
        self._from_version = from_version

    @property
    def to_version(self) -> str | None:
        return self._to_version

    @to_version.setter
    def to_version(self, to_version: str | None) -> None:
        self._to_version = to_version

    @property
    def flows(self) -> list[str]:
        return self._flows

    @flows.setter
    def flows(self, flows: list[str]) -> None:
        self._flows = flows

    @property
    def project(self) -> str | None:
        return self._project

    @project.setter
    def project(self, project: str | None) -> None:
        self._project = project

    @property
    def pull_request_id(self) -> str | None:
        return self._pull_request_id

    @pull_request_id.setter
    def pull_request_id(self, pull_request_id: str | None) -> None:
        self._pull_request_id = pull_request_id

    def add_flows(self, curr_flows: list[str] | None):
        Utils.add_flows_without_duplications(self.flows, curr_flows)

    def serialize(self) -> dict[str, Any]:
        return Utils.serialize_class(self, [])

    @staticmethod
    def create():
        return ServiceDataBuilder()


class ServiceDataBuilder(Builder[ServiceData]):
    def __init__(self, service_data=None):
        service_data = service_data if service_data is not None else ServiceData()
        super().__init__(service_data)

    def from_version(self, from_version: str | None) -> ServiceDataBuilder:
        self._item.from_version = from_version
        return self

    def to_version(self, to_version: str | None) -> ServiceDataBuilder:
        self._item.to_version = to_version
        return self

    def flows(self, flows: list[str]) -> ServiceDataBuilder:
        self._item.flows = flows
        return self

    def project(self, project: str | None) -> ServiceDataBuilder:
        self._item.project = project
        return self

    def pull_request_id(self, pull_request_id: str | None) -> ServiceDataBuilder:
        self._item.pull_request_id = pull_request_id
        return self
