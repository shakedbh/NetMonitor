import netifaces as ni
import psutil
from Functions import Functions
from logger import Logger


class Network:
    def __init__(self):
        self.functions = Functions()
        self.logger = Logger(self.__class__.__name__)

    def get_running_interface(self):
        """
        This function return the name of the running interface.
        :return: The name of the running interface or None.
        """
        try:
            gateway_info = ni.gateways()
            if NetworkArguments.DEFAULT in gateway_info and ni.AF_INET in gateway_info[NetworkArguments.DEFAULT]:
                return gateway_info[NetworkArguments.DEFAULT][ni.AF_INET][NetworkArguments.INDEX_OF_NAME_INTERFACE]

        except Exception as err:
            self.logger.logger.error(f"Unable to return the running interface, Error: {err}")
            return None

    def validate_running_interface_status(self, interface):
        """
        This function checks the status of the running interface.
        :param interface: The name of the running interface.
        :return: True if the interface is UP, and false otherwise.
        """
        try:
            all_interfaces = psutil.net_if_stats().keys()
            if interface in all_interfaces:
                interface_status = psutil.net_if_stats()[interface].isup
                return interface_status
            return False

        except Exception as err:
            self.logger.logger.error(err)
            raise NetworkError(f"Unable to validate the running interface status, Error: {err}")


class NetworkArguments:
    DEFAULT = 'default'
    INDEX_OF_NAME_INTERFACE = 1


class NetworkError(Exception):
    pass
