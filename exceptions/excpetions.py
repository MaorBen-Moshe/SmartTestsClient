class SmartClientBaseException(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code


class BadRequest(SmartClientBaseException):
    def __init__(self, message: str):
        super().__init__(message, 400)


class NotFoundError(SmartClientBaseException):
    def __init__(self, message: str):
        super().__init__(message, 500)


class EmptyInputError(SmartClientBaseException):
    def __init__(self, message: str):
        super().__init__(message, 500)
