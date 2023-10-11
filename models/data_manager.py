from __future__ import annotations

from constants.constants import *
from models.group_data import GroupData
from models.service_data import ServiceData


class DataManager:

    def __init__(self):
        self.curr_group: str | None = None
        self.services_map: dict[str, ServiceData] | None = {}
        self.__filter_by_group: dict[str, list[str]] = {
            "oc-cd-group4-coc-include-ed": GROUP4_XML,
        }
        self.groups_data: dict[str, GroupData] = {}

    def set_curr_group(self, group_name: str | None):
        self.curr_group = group_name

    def get_filter_for_curr_group(self):
        return self.__filter_by_group.get(self.curr_group)
