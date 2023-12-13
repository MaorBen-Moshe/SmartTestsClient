from __future__ import annotations
from typing import TypeVar, Generic

T = TypeVar("T")


class DictWrapperObject(Generic[T]):
    def __init__(self):
        self.map: dict[str, T] = {}

    def add_item(self, key: str, value: T):
        if key:
            self.map[key] = value

    def get_item(self, key: str) -> T:
        return self.map.get(key)

    def contains_key(self, key: str) -> bool:
        return key in self.map

    def merge(self, other: DictWrapperObject[T]):
        self.map.update(other.map)

    def __iter__(self):
        return iter(self.map)

    def __len__(self):
        return len(self.map)
