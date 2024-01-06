from typing import TypeVar, Generic

T = TypeVar("T")


class Builder(Generic[T]):

    __slots__ = ["_item"]

    def __init__(self, item: T):
        self._item = item

    def build(self) -> T:
        return self._item
