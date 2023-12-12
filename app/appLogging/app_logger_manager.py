from __future__ import annotations

import logging
import os

from app.appLogging.app_logger import AppLogger
from app.models.singleton_meta import SingletonMeta


class AppLoggerManager(metaclass=SingletonMeta):
    def __init__(self):
        self._loggers: dict[str, AppLogger] = {}
        self._formatter = logging.Formatter('[%(levelname)s] [%(trace_id)s] [%(asctime)s] %(message)s')

    def init_logger(self,
                    logger,
                    log_level,
                    log_file_path,
                    log_file_name,
                    trace_id_filter):
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

        # Add the file and console handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        _logger = AppLogger(logger)
        self._loggers[logger.name] = _logger

    def get_logger(self, logger_name: str) -> AppLogger:
        if logger_name not in self._loggers:
            raise ValueError(f"Logger {logger_name} does not exist, please init it first.")
        app_logger = self._loggers[logger_name]
        return app_logger

    @staticmethod
    def __init_file_handler_path(log_file_path: str, log_file_name: str) -> str:
        if os.path.exists(log_file_path) is False:
            os.mkdir(log_file_path)

        if os.path.exists(os.path.join(log_file_path, log_file_name)) is False:
            with open(os.path.join(log_file_path, log_file_name), "w") as f:
                f.write("")
        else:
            with open(os.path.join(log_file_path, log_file_name), "r+") as f:
                f.truncate(0)

        return os.path.join(log_file_path, log_file_name)
