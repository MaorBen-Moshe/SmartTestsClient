from __future__ import annotations
from typing import TypeVar, Generic

T = TypeVar("T")


class DictWrapperObject(Generic[T]):

    __slots__ = ["_map"]

    def __init__(self):
        self._map: dict[str, T] = {}

    def add_item(self, key: str, value: T):
        if key:
            self._map[key] = value

    def get_item(self, key: str) -> T:
        return self._map.get(key)

    def contains_key(self, key: str) -> bool:
        return key in self._map

    def merge(self, other: DictWrapperObject[T]):
        self._map.update(other._map)

    def __iter__(self):
        return iter(self._map)

    def __len__(self):
        return len(self._map)

    def __str__(self):
        return self._map.__str__() if self._map else ""
