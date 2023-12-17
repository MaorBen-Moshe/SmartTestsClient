from __future__ import annotations

from http import HTTPStatus


class SmartClientBaseException(Exception):
    def __init__(self, message: str | None, code: int):
        super().__init__(f"{code}: {message}")
        self.code = code


class BadRequest(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, HTTPStatus.BAD_REQUEST.value)


class NotFoundError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, HTTPStatus.NOT_FOUND.value)


class EmptyInputError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, HTTPStatus.INTERNAL_SERVER_ERROR.value)


class ConfigurationError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, HTTPStatus.INTERNAL_SERVER_ERROR.value)


class URLError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, HTTPStatus.INTERNAL_SERVER_ERROR.value)


class BadGatewayError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, HTTPStatus.BAD_GATEWAY.value)
