from __future__ import annotations

from app.models.builder import Builder


class ServiceData:
    def __init__(self):
        self.from_version = None
        self.to_version = None

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

    @staticmethod
    def create():
        return ServiceDataBuilder()


class ServiceDataBuilder(Builder[ServiceData]):
    def __init__(self, service_data=None):
        service_data = service_data if service_data is not None else ServiceData()
        super().__init__(service_data)

    def from_version(self, from_version: str | None) -> ServiceDataBuilder:
        self.item.from_version = from_version
        return self

    def to_version(self, to_version: str | None) -> ServiceDataBuilder:
        self.item.to_version = to_version
        return self
