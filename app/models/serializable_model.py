from __future__ import annotations

from abc import ABC
from typing import Any


class Serializable(ABC):

    def toJSON(self) -> dict[str, Any] | None:
        if self is None:
            return None

        result = {}
        for i, value in self.__dict__.items():
            key = i.replace(self.__class__.__name__, '').lstrip("_")
            if isinstance(value, Serializable):  # check if the value is a class type
                value = getattr(value, "toJSON")()  # call the toJSON method on the value
            elif isinstance(value, list) and all(
                    isinstance(item, Serializable) for item in value):  # check if the value is a list of class objects
                value = [getattr(item, "toJSON")() for item in value]  # call the toJSON method on each item
            elif isinstance(value, tuple) and all(
                    isinstance(item, Serializable) for item in value):  # check if the value is a tuple of class objects
                value = tuple(getattr(item, "toJSON")() for item in value)  # call the toJSON method on each item
            elif isinstance(value, dict) and all(
                    isinstance(item, Serializable) for item in
                    value.values()):  # check if the value is a dict of class objects
                value = {k: getattr(item, "toJSON")() for k, item in
                         value.items()}  # call the toJSON method on each value
            result[key] = value
        return result
