from __future__ import annotations

from app.models.service_data import ServiceData


class ServicesData:
    def __init__(self):
        self.__services_map: dict[str, ServiceData] = {}

    def add_service(self, service_name: str, service: ServiceData):
        if service_name:
            self.__services_map[service_name] = service

    def get_service(self, service_name: str) -> ServiceData:
        return self.__services_map.get(service_name)

    def merge(self, other: ServicesData):
        if other:
            for service_name in other:
                self.add_service(service_name, other.get_service(service_name))

    def __iter__(self):
        return iter(self.__services_map)

    def __len__(self):
        return len(self.__services_map)
