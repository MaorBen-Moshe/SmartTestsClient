from __future__ import annotations

from constants.constants import *
from models.group_data import GroupData
from models.service_data import ServiceData


class DataManager:

    def __init__(self):
        self.curr_group: str | None = None
        self.services_map: dict[str, ServiceData] | None = {}
        self.groups_data: dict[str, GroupData] = {}
        self.__filter_by_group: dict[str, list[str]] = {
            "oc-cd-group4-coc-include-ed": GROUP4_XML,
        }

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
    def filter_for_curr_group(self):
        return self.__filter_by_group.get(self.curr_group)
