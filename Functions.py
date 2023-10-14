from json import load
from os import path, makedirs
from logger import Logger


class Functions:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    def bytes_to_mbps(self, bytes_value: float) -> float:
        """
        This function converts from bytes/s to Mbps.
        :param bytes_value: The value in bytes/s.
        :return: The value in Mbps.
        """
        mb_value = bytes_value / FunctionsArguments.CONVERT_TO_MB
        return mb_value

    def get_data_json(self, file_path: str) -> dict:
        """
        This function gets the data from a json file.
        :param file_path: The path to a json file.
        :return: The data.
        """
        try:
            with open(file_path, FunctionsArguments.READ_MODE) as json_file:
                data = load(json_file)
            return data

        except Exception as err:
            self.logger.logger.error(err)
            raise FunctionsError(f"Unable to return data, Error: {err}")

    def set_config_mode(self, config_value: str) -> bool:
        """
        This function returns TRUE/FALSE value according to parameters in a config file.
        :param config_value: The value of the parameter.
        :return: True if the value is: "true", False if the value is: "false".
        """
        try:
            if config_value == FunctionsArguments.TRUE.lower():
                return True
            elif config_value == FunctionsArguments.FALSE.lower():
                return False

        except Exception as err:
            self.logger.logger.error(err)
            raise FunctionsError(f"Error while setting a config mode: {err}")

    def create_dir(self, dir_name: str) -> None:
        """
        This function checks if dir_name directory exists, if not it creates a directory.
        :param dir_name: The name of directory.
        :return: None
        """
        try:
            if not path.exists(dir_name):
                makedirs(dir_name, exist_ok=True)

        except Exception as err:
            self.logger.logger.error(err)
            raise FunctionsError(f"Error while creating '{dir_name}' directory: {err}")


class FunctionsArguments:

    TRUE = "true"
    FALSE = "false"

    # config.json file
    CONFIG_JSON_PATH = "/home/dev/PycharmProjects/NetMonitorr/config.json"
    LOW_LIMIT = "low_limit"
    HIGH_LIMIT = "high_limit"
    SAVE_GRAPHS = "save_graphs"
    SHOW_GRAPHS = "show_graphs"
    TIME_INTERVAL = "time_interval"
    DEV_MODE = "dev_mode"
    CLEAN_FOLDER = "clean_folder"

    CONVERT_TO_MB = 125000

    # files
    READ_MODE = 'r'


class FunctionsError(Exception):
    pass
