from __future__ import annotations


class SmartClientBaseException(Exception):
    def __init__(self, message: str | None, code: int, level: str = 'ERROR'):
        super().__init__(f"[{level}] {code}: {message}")
        self.code = code


class BadRequest(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, 400)


class NotFoundError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, 404)


class EmptyInputError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, 500)


class ConfigurationError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, 500)


class URLError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, 500)
