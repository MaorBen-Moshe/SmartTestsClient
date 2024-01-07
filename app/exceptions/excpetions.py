from __future__ import annotations

from http import HTTPStatus


class SmartClientBaseException(Exception):
    """A base class for all custom exceptions raised by the Smart Client."""

    def __init__(self, message: str | None, code: int):
        """Initializes the exception with a message and an HTTP status code.

        Args:
            message (str | None): The message to display, or None.
            code (int): The HTTP status code to return.
        """
        super().__init__(f"{code}: {message}")
        self.code = code


class BadRequest(SmartClientBaseException):
    """An exception that indicates a bad request from the client."""

    def __init__(self, message: str | None):
        """Initializes the exception with a message and a 400 status code.

        Args:
            message (str | None): The message to display, or None.
        """
        super().__init__(message, HTTPStatus.BAD_REQUEST.value)


class NotFoundError(SmartClientBaseException):
    """An exception that indicates a resource not found on the server."""

    def __init__(self, message: str | None):
        """Initializes the exception with a message and a 404 status code.

        Args:
            message (str | None): The message to display, or None.
        """
        super().__init__(message, HTTPStatus.NOT_FOUND.value)


class EmptyInputError(SmartClientBaseException):
    """An exception that indicates an empty input from the client."""

    def __init__(self, message: str | None):
        """Initializes the exception with a message and a 500 status code.

        Args:
            message (str | None): The message to display, or None.
        """
        super().__init__(message, HTTPStatus.INTERNAL_SERVER_ERROR.value)


class ConfigurationError(SmartClientBaseException):
    """An exception that indicates a configuration error on the server."""

    def __init__(self, message: str | None):
        """Initializes the exception with a message and a 500 status code.

        Args:
            message (str | None): The message to display, or None.
        """
        super().__init__(message, HTTPStatus.INTERNAL_SERVER_ERROR.value)


class URLError(SmartClientBaseException):
    """An exception that indicates an invalid or unsupported URL."""

    def __init__(self, message: str | None):
        """Initializes the exception with a message and a 500 status code.

        Args:
            message (str | None): The message to display, or None.
        """
        super().__init__(message, HTTPStatus.INTERNAL_SERVER_ERROR.value)


class BadGatewayError(SmartClientBaseException):
    """An exception that indicates a bad gateway error on the server."""

    def __init__(self, message: str | None):
        """Initializes the exception with a message and a 502 status code.

        Args:
            message (str | None): The message to display, or None.
        """
        super().__init__(message, HTTPStatus.BAD_GATEWAY.value)
