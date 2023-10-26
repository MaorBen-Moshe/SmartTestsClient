from __future__ import annotations


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


class ServiceDataBuilder:
    def __init__(self):
        self.service_data = ServiceData()

    def build(self) -> ServiceData:
        return self.service_data

    def old_version(self, old_version: str | None) -> ServiceDataBuilder:
        self.service_data.old_version = old_version
        return self

    def new_version(self, new_version: str | None) -> ServiceDataBuilder:
        self.service_data.new_version = new_version
        return self
