from __future__ import annotations


class SmartClientBaseException(Exception):
    def __init__(self, message: str | None, code: int):
        super().__init__(message)
        self.code = code


class BadRequest(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, 400)


class NotFoundError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, 500)


class EmptyInputError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, 500)


class ConfigurationError(SmartClientBaseException):
    def __init__(self, message: str | None):
        super().__init__(message, 500)
