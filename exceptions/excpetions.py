class BaseException(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code


class BadRequest(BaseException):
    def __init__(self, message: str):
        super().__init__(message, 400)


class NotFoundError(BaseException):
    def __init__(self, message: str):
        super().__init__(message, 500)


class EmptyInputError(BaseException):
    def __init__(self, message: str):
        super().__init__(message, 500)
