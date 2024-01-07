class AppLogger:
    """AppLogger class is a wrapper of logging.Logger class."""
    def __init__(self, logger):
        self._logger = logger

    def get_logger_name(self) -> str:
        """Get the name of the logger."""
        return self._logger.name

    def debug(self, message: str):
        """Log a message with severity 'DEBUG' on this logger."""
        self._logger.debug(message)

    def info(self, message: str):
        """Log a message with severity 'INFO' on this logger."""
        self._logger.info(message)

    def warning(self, message: str):
        """Log a message with severity 'WARNING' on this logger."""
        self._logger.warning(message)

    def error(self, message: str):
        """Log a message with severity 'ERROR' on this logger."""
        self._logger.error(message)

    def critical(self, message: str):
        """Log a message with severity 'CRITICAL' on this logger."""
        self._logger.critical(message)
