from __future__ import annotations

from app.models.group_data import GroupData
from app.models.services_data import ServicesData


class DataManager:
    def __init__(self):
        self.services_map: ServicesData | None = ServicesData()
        self.groups_data: dict[str, GroupData] = {}

    @property
    def services_map(self) -> ServicesData | None:
        return self._services_map

    @services_map.setter
    def services_map(self, services_map: ServicesData):
        self._services_map = services_map

    @property
    def groups_data(self) -> dict[str, GroupData]:
        return self._groups_data

    @groups_data.setter
    def groups_data(self, groups_data: dict[str, GroupData]):
        self._groups_data = groups_data
