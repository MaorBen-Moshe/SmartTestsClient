from __future__ import annotations
from typing import TypeVar, Generic

T = TypeVar("T")


class DictWrapperObject(Generic[T]):
    """A generic class that wraps a dictionary of type T."""

    __slots__ = ["_map"]

    def __init__(self):
        """Initializes the wrapper with an empty dictionary of type T."""
        self._map: dict[str, T] = {}

    def add_item(self, key: str, value: T):
        """Adds an item to the dictionary with the given key and value.

        Args:
            key (str): The key of the item to add.
            value (T): The value of the item to add.
        """
        if key:
            self._map[key] = value

    def get_item(self, key: str) -> T:
        """Gets the item from the dictionary with the given key.

        Args:
            key (str): The key of the item to get.

        Returns:
            T: The value of the item, or None if the key does not exist.
        """
        return self._map.get(key)

    def contains_key(self, key: str) -> bool:
        """Checks if the dictionary contains the given key.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return key in self._map

    def merge(self, other: DictWrapperObject[T]):
        """Merges the dictionary with another dictionary wrapper of the same type.

        Args:
            other (DictWrapperObject[T]): The other dictionary wrapper to merge with.
        """
        self._map.update(other._map)

    def __iter__(self):
        """Returns an iterator over the keys of the dictionary.

        Returns:
            Iterator[str]: An iterator over the keys of the dictionary.
        """
        return iter(self._map)

    def __len__(self):
        """Returns the length of the dictionary.

        Returns:
            int: The number of items in the dictionary.
        """
        return len(self._map)

    def __str__(self):
        """Returns the string representation of the dictionary.

        Returns:
            str: The string representation of the dictionary, or an empty string if the dictionary is empty.
        """
        return self._map.__str__() if self._map else ""
