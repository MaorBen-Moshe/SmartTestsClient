from __future__ import annotations

import logging
import os

from app.appLogging.app_logger import AppLogger
from app.models.singleton_meta import SingletonMeta


class AppLoggerManager(metaclass=SingletonMeta):
    """A class that manages the application loggers."""

    def __init__(self):
        """Initializes the logger manager with an empty dictionary of loggers and a formatter."""
        self._loggers: dict[str, AppLogger] = {}
        self._formatter = logging.Formatter('[%(levelname)s] [%(trace_id)s] [%(asctime)s] %(message)s')

    def init_logger(self,
                    logger,
                    log_level,
                    log_file_path,
                    log_file_name,
                    trace_id_filter):
        """Initializes a logger with the given parameters and adds it to the dictionary of loggers.

        Args:
            logger: The logger to initialize.
            log_level: The log level to set for the logger.
            log_file_path: The path of the log file to write to.
            log_file_name: The name of the log file to write to.
            trace_id_filter: The filter to apply to the logger for the trace ID.
        """
        log_level = logging.getLevelName(log_level)
        logger.setLevel(log_level)

        file_handler = logging.FileHandler(self.__init_file_handler_path(log_file_path, log_file_name))
        file_handler.addFilter(trace_id_filter)
        file_handler.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.addFilter(trace_id_filter)
        console_handler.setLevel(log_level)

        file_handler.setFormatter(self._formatter)
        console_handler.setFormatter(self._formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        _logger = AppLogger(logger)
        self._loggers[logger.name] = _logger

    def get_logger(self, logger_name: str) -> AppLogger:
        """Gets the logger with the given name from the dictionary of loggers.

        Args:
            logger_name (str): The name of the logger to get.

        Returns:
            AppLogger: The logger with the given name, or None if not found.

        Raises:
            ValueError: If the logger name does not exist in the dictionary of loggers.
        """
        if logger_name not in self._loggers:
            raise ValueError(f"Logger {logger_name} does not exist, please init it first.")
        app_logger = self._loggers[logger_name]
        return app_logger

    @classmethod
    def __init_file_handler_path(cls, log_file_path: str, log_file_name: str) -> str:
        """Initializes the file handler path for the logger by creating the directory and file if they do not exist.

        Args:
            log_file_path (str): The path of the log file to write to.
            log_file_name (str): The name of the log file to write to.

        Returns:
            str: The full path of the log file.
        """
        if os.path.exists(log_file_path) is False:
            os.mkdir(log_file_path)

        if os.path.exists(os.path.join(log_file_path, log_file_name)) is False:
            with open(os.path.join(log_file_path, log_file_name), "w") as f:
                f.write("")
        else:
            with open(os.path.join(log_file_path, log_file_name), "r+") as f:
                f.truncate(0)

        return os.path.join(log_file_path, log_file_name)
