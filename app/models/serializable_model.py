from __future__ import annotations

from abc import ABC
from typing import Any


class Serializable(ABC):
    """An abstract base class that defines a method for serializing an object to a JSON dictionary."""

    __slots__ = ()

    def toJSON(self, ignore_none=True) -> dict[str, Any] | None:
        """Serializes the object to a JSON dictionary.

        Args:
            ignore_none (bool): Whether to ignore None values or not. Defaults to True.

        Returns:
            dict[str, Any] | None: The JSON dictionary, or None if the object is None.
        """
        if self is None:
            return None

        result = {}
        for i in self.__slots__:
            value = getattr(self, i)
            key = i.lstrip("_")
            if isinstance(value, Serializable):
                value = getattr(value, "toJSON")()
            elif isinstance(value, list) and all(isinstance(item, Serializable) for item in value):
                value = [getattr(item, "toJSON")() for item in value]
                value = value if len(value) > 0 else None
            elif isinstance(value, tuple) and all(isinstance(item, Serializable) for item in value):
                value = tuple(getattr(item, "toJSON")() for item in value)
                value = value if len(value) > 0 else None
            elif isinstance(value, dict) and all(isinstance(item, Serializable) for item in value.values()):
                value = {k: getattr(item, "toJSON")() for k, item in value.items()}
                value = value if len(value) > 0 else None

            if value is not None or not ignore_none:
                result[key] = value

        return result
