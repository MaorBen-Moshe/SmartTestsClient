from __future__ import annotations

from app.models.builder import Builder
from app.models.serializable_model import Serializable


class Error(Serializable):
    """A class that represents an error with a code, a message, a timestamp, and a trace ID."""

    __slots__ = ["_error_code", "_error_message", "_timestamp", "_trace_id"]

    def __init__(self):
        """Initializes the error with None values for the attributes."""
        self.error_code: int | None = None
        self.error_message: str | None = None
        self.timestamp: str | None = None
        self.trace_id: str | None = None

    @property
    def error_code(self) -> int | None:
        """Gets or sets the error code.

        Returns:
            int | None: The error code, or None if not set.
        """
        return self._error_code

    @error_code.setter
    def error_code(self, error_code: int | None):
        """Sets the error code.

        Args:
            error_code (int | None): The error code, or None to unset it.
        """
        self._error_code = error_code

    @property
    def error_message(self) -> str | None:
        """Gets or sets the error message.

        Returns:
            str | None: The error message, or None if not set.
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message: str | None):
        """Sets the error message.

        Args:
            error_message (str | None): The error message, or None to unset it.
        """
        self._error_message = error_message

    @property
    def timestamp(self) -> str | None:
        """Gets or sets the timestamp of the error.

        Returns:
            str | None: The timestamp of the error, or None if not set.
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: str | None):
        """Sets the timestamp of the error.

        Args:
            timestamp (str | None): The timestamp of the error, or None to unset it.
        """
        self._timestamp = timestamp

    @property
    def trace_id(self) -> str | None:
        """Gets or sets the trace ID of the error.

        Returns:
            str | None: The trace ID of the error, or None if not set.
        """
        return self._trace_id

    @trace_id.setter
    def trace_id(self, trace_id: str | None):
        """Sets the trace ID of the error.

        Args:
            trace_id (str | None): The trace ID of the error, or None to unset it.
        """
        self._trace_id = trace_id

    @staticmethod
    def create():
        """Creates a new error builder.

        Returns:
            ErrorModelBuilder: An error builder instance.
        """
        return ErrorModelBuilder()


class ErrorModelBuilder(Builder[Error]):
    """A class that builds an error instance."""

    def __init__(self, error=None):
        """Initializes the error builder with an error instance.

        Args:
            error (Error | None): The error instance to build, or None to create a new one.
        """
        error = error if error else Error()
        super().__init__(error)

    def error_code(self, error_code: int | None) -> ErrorModelBuilder:
        """Sets the error code of the error to build.

        Args:
            error_code (int | None): The error code, or None to unset it.

        Returns:
            ErrorModelBuilder: The same error builder instance, for method chaining.
        """
        self._item.error_code = error_code
        return self

    def error_message(self, error_message: str | None) -> ErrorModelBuilder:
        """Sets the error message of the error to build.

        Args:
            error_message (str | None): The error message, or None to unset it.

        Returns:
            ErrorModelBuilder: The same error builder instance, for method chaining.
        """
        self._item.error_message = error_message
        return self

    def timestamp(self, timestamp: str | None) -> ErrorModelBuilder:
        """Sets the timestamp of the error to build.

        Args:
            timestamp (str | None): The timestamp of the error, or None to unset it.

        Returns:
            ErrorModelBuilder: The same error builder instance, for method chaining.
        """
        self._item.timestamp = timestamp
        return self

    def trace_id(self, trace_id: str | None) -> ErrorModelBuilder:
        """Sets the trace ID of the error to build.

        Args:
            trace_id (str | None): The trace ID of the error, or None to unset it.

        Returns:
            ErrorModelBuilder: The same error builder instance, for method chaining.
        """
        self._item.trace_id = trace_id
        return self
