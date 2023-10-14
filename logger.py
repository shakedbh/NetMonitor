from logging import getLogger, basicConfig, DEBUG, INFO
from os import path


class Logger:
    """Custom logger class"""

    def __init__(self, logger_name: str):
        self.logger = getLogger(logger_name)
        self.log_file_mode = self.set_log_file_mode()
        self.log_level = self.set_log_level(False)
        basicConfig(filename=LoggerArguments.LOG_FILE_PATH, filemode=self.log_file_mode,
                    format=LoggerArguments.LOG_FILE_FORMAT, level=self.log_level,
                    datefmt=LoggerArguments.LOG_DATE_FORMAT)

    def set_log_file_mode(self) -> str:
        """
        This function sets the log file mode.
        :return: The mode, 'a' for append, 'w' for write.
        """
        try:
            if path.exists(LoggerArguments.LOG_FILE_PATH):
                return LoggerArguments.APPEND_MODE
            else:
                return LoggerArguments.WRITE_MODE

        except Exception as err:
            raise LoggerError(f"Unable to set {self.__class__.__name__} log file mode, Error: {err}")

    def set_log_level(self, mode: bool) -> int:
        """
        This function sets the log level.
        :param mode: A boolean variable. True to debug mode, False to info mode.
        :return: The log level.
        """
        try:
            if mode:
                return DEBUG
            else:
                return INFO

        except Exception as err:
            raise LoggerError(f"Unable to set {self.__class__.__name__} log level, Error: {err}")


class LoggerArguments:
    # log file
    LOG_FILE_PATH = "/home/dev/PycharmProjects/NetMonitorr/net_monitor.log"
    LOG_FILE_FORMAT = "[%(asctime)s] - [%(name)s] - [%(levelname)s] --- %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    APPEND_MODE = 'a'
    WRITE_MODE = 'w'


class LoggerError(Exception):
    pass
