from __future__ import annotations

import logging
import os

from app.models.singleton_meta import SingletonMeta


class AppLogger(metaclass=SingletonMeta):
    _loggers: dict[str, AppLogger] = {}
    _formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s')

    def __init__(self):
        self._logger = None

    @classmethod
    def init_logger(cls, logger, log_level, log_file_path, log_file_name):
        log_level = logging.getLevelName(log_level)
        logger.setLevel(log_level)

        file_handler = logging.FileHandler(cls.__init_file_handler_path(log_file_path, log_file_name))
        file_handler.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        file_handler.setFormatter(cls._formatter)
        console_handler.setFormatter(cls._formatter)

        # Add the file and console handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        _logger = AppLogger()
        _logger._logger = logger
        cls._loggers[logger.name] = _logger

    @classmethod
    def get_logger(cls, logger_name: str) -> AppLogger:
        if logger_name not in cls._loggers:
            raise ValueError(f"Logger {logger_name} does not exist, please init it first.")
        app_logger = cls._loggers[logger_name]
        return app_logger

    def debug(self, message: str):
        self._logger.debug(message)

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def critical(self, message: str):
        self._logger.critical(message)

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
