from __future__ import annotations

from app import config
from app.models.group_data import GroupData
from app.models.service_data import ServiceData


class DataManager:

    def __init__(self):
        self.curr_group: str | None = None
        self.services_map: dict[str, ServiceData] | None = {}
        self.groups_data: dict[str, GroupData] = {}

    @property
    def curr_group(self) -> str | None:
        return self._curr_group

    @curr_group.setter
    def curr_group(self, group_name: str | None):
        self._curr_group = group_name

    @property
    def services_map(self) -> dict[str, ServiceData] | None:
        return self._services_map

    @services_map.setter
    def services_map(self, services_map: dict[str, ServiceData] | None):
        self._services_map = services_map

    @property
    def groups_data(self) -> dict[str, GroupData]:
        return self._groups_data

    @groups_data.setter
    def groups_data(self, groups_data: dict[str, GroupData]):
        self._groups_data = groups_data

    @property
    def filter_for_curr_group(self) -> list[str]:
        return config.get_supported_groups().get(self.curr_group).testng_xml
