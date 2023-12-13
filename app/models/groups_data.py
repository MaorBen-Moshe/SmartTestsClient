from __future__ import annotations

from app.models.group_data import GroupData


class TestGroupsData:
    def __init__(self):
        self.__groups_map: dict[str, GroupData] = {}

    def add_group(self, group_name: str, group: GroupData):
        if group_name not in self.__groups_map:
            self.__groups_map[group_name] = group

    def get_group(self, group_name: str) -> GroupData:
        return self.__groups_map.get(group_name)

    def merge(self, other: TestGroupsData):
        if other:
            for group_name in other:
                self.add_group(group_name, other.get_group(group_name))

    def __iter__(self):
        return iter(self.__groups_map)

    def __len__(self):
        return len(self.__groups_map)
