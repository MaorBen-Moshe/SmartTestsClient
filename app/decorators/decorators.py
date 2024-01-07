from functools import wraps

from app import app_main_logger
from app.exceptions.excpetions import BadGatewayError, SmartClientBaseException


def gateway_errors_handler(func):
    """A decorator that handles gateway errors for a function.

    Args:
        func: The function to decorate.

    Returns:
        A wrapper function that catches and logs SmartClientBaseException and other exceptions, and raises BadGatewayError instead.
    """
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
    """A decorator factory that creates a decorator that logs the arguments and output of a function.

    Args:
        print_output (bool): Whether to print the output of the function or not. Defaults to False.

    Returns:
        A decorator that wraps a function with logging statements.
    """
    def inner(func):
        """The actual decorator that logs the arguments and output of a function.

        Args:
            func: The function to decorate.

        Returns:
            A wrapper function that logs the class name, function name, arguments, and output of the function.
        """
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
