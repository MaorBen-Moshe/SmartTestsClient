from threading import Lock


class SingletonMeta(type):
    """A metaclass that implements the singleton design pattern."""

    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """Creates or returns the singleton instance of the class.

        Args:
            *args: The positional arguments for the class constructor.
            **kwargs: The keyword arguments for the class constructor.

        Returns:
            The singleton instance of the class.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
