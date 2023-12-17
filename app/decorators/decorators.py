from functools import wraps

from app import app_main_logger
from app.exceptions.excpetions import BadGatewayError, SmartClientBaseException


def gatewayErrorsHandler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SmartClientBaseException as e:
            app_main_logger.error(f"Error occurred: {e}")
            raise e
        except Exception as e:
            app_main_logger.error(f"Error occurred: {e}")
            raise BadGatewayError(e.__str__())

    return wrapper


def log_around(print_output=False):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            class_name = ""
            is_class_method = False
            if args and hasattr(args[0], func.__name__):
                is_class_method = True
                class_name = f"{args[0].__class__.__name__}."

            func_name = func.__name__

            if is_class_method:
                func_args = ", ".join(repr(arg) for arg in args[1:]) + ", " + ", ".join(
                    f"{key}={value}" for key, value in kwargs.items())
            else:
                func_args = ", ".join(repr(arg) for arg in args) + ", " + ", ".join(
                    f"{key}={value!r}" for key, value in kwargs.items())

            app_main_logger.debug(f"{class_name}{func_name}: {func_args}")
            result = func(*args, **kwargs)
            if print_output:
                app_main_logger.debug(f"{class_name}{func_name}: {result!r}")

            return result

        return wrapper

    return inner
