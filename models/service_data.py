from __future__ import annotations


class ServiceData:
    def __init__(self):
        self.old_version: str = ""
        self.new_version: str = ""


class ServiceDataBuilder:
    def __init__(self):
        self.service_data = ServiceData()

    def build(self) -> ServiceData:
        return self.service_data

    def old_version(self, old_version: str) -> ServiceDataBuilder:
        self.service_data.old_version = old_version
        return self

    def new_version(self, new_version: str) -> ServiceDataBuilder:
        self.service_data.new_version = new_version
        return self
