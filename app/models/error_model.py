from __future__ import annotations

from app.models.builder import Builder
from app.utils.utils import Utils


class Error:
    def __init__(self):
        self.error_code: int | None = None
        self.error_message: str | None = None
        self.timestamp: str | None = None

    def serialize(self) -> dict[str, str | int]:
        return Utils.serialize_class(self, [])

    @property
    def error_code(self) -> int | None:
        return self._error_code

    @error_code.setter
    def error_code(self, error_code: int | None):
        self._error_code = error_code

    @property
    def error_message(self) -> str | None:
        return self._error_message

    @error_message.setter
    def error_message(self, error_message: str | None):
        self._error_message = error_message

    @property
    def timestamp(self) -> str | None:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: str | None):
        self._timestamp = timestamp

    @staticmethod
    def create():
        return ErrorModelBuilder()


class ErrorModelBuilder(Builder[Error]):
    def __init__(self, error=None):
        error = error if error else Error()
        super().__init__(error)

    def error_code(self, error_code: int | None) -> ErrorModelBuilder:
        self.item.error_code = error_code
        return self

    def error_message(self, error_message: str | None) -> ErrorModelBuilder:
        self.item.error_message = error_message
        return self

    def timestamp(self, timestamp: str | None) -> ErrorModelBuilder:
        self.item.timestamp = timestamp
        return self