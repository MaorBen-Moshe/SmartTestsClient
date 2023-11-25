from __future__ import annotations

from app.models.builder import Builder


class ServiceData:
    def __init__(self):
        self.old_version = None
        self.new_version = None

    @property
    def old_version(self) -> str | None:
        return self._old_version

    @old_version.setter
    def old_version(self, old_version: str | None) -> None:
        self._old_version = old_version

    @property
    def new_version(self) -> str | None:
        return self._new_version

    @new_version.setter
    def new_version(self, new_version: str | None) -> None:
        self._new_version = new_version

    @staticmethod
    def create():
        return ServiceDataBuilder()


class ServiceDataBuilder(Builder):
    def __init__(self, service_data=None):
        service_data = service_data if service_data is not None else ServiceData()
        super().__init__(service_data)

    def old_version(self, old_version: str | None) -> ServiceDataBuilder:
        self.item.old_version = old_version
        return self

    def new_version(self, new_version: str | None) -> ServiceDataBuilder:
        self.item.new_version = new_version
        return self
