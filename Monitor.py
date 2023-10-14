import datetime
import matplotlib.pyplot as plt
from Network import Network
from Functions import Functions
from Functions import FunctionsArguments
from os import path
from speedtest import Speedtest
from logger import Logger


class Monitor:
    def __init__(self) -> None:
        self.functions = Functions()
        self.network = Network()
        self.sent_rates = []
        self.recv_rates = []
        self.alert_msg = None
        self.date_time = datetime
        self.logger = Logger(self.__class__.__name__)

    def calculate_connection_rate_speedtest(self, time_interval: int) -> None:
        """
        This funtion calculates the connection rate using speedtest-cli library.
        :return: None
        """
        try:
            minutes = time_interval / MonitorArguments.ONE_MINUTE_IN_SECONDS
            minute_duration = self.date_time.timedelta(minutes=minutes)
            start_time = self.date_time.datetime.now()
            end_time = start_time + minute_duration

            # This loop runs for time_interval and fills the buffer
            while self.date_time.datetime.now() < end_time:
                st = Speedtest()
                st.get_best_server()

                # in bits
                download_speed = st.download(threads=MonitorArguments.THREADS_DEFAULT)
                upload_speed = st.upload(threads=MonitorArguments.THREADS_DEFAULT)

                # convert to bytes/s
                download_rate = download_speed / MonitorArguments.CONVERSION_NUMBER
                upload_rate = upload_speed / MonitorArguments.CONVERSION_NUMBER

                # convert to Mbps
                mb_sent_rate = self.functions.bytes_to_mbps(upload_rate)
                mb_recv_rate = self.functions.bytes_to_mbps(download_rate)

                # fill the buffer
                self.sent_rates.append(mb_sent_rate)
                self.recv_rates.append(mb_recv_rate)

        except Exception as err:
            self.logger.logger.error(err)

    def alert_user(self, sent_rate: float, recv_rate: float, low_limit: float, high_limit: float,
                   interface_status: bool) -> None:
        """
        This function alerts to user
        :param sent_rate: The current sent rate.
        :param recv_rate: The current received rate.
        :param low_limit: The minimum acceptable connection rate.
        :param high_limit: The maximum acceptable connection rate.
        :param interface_status: The status of the running interface
        :return: None
        """
        try:
            if not interface_status:
                self.alert_msg = MonitorArguments.INTERFACE_DOWN

            elif sent_rate < low_limit or recv_rate < low_limit:
                self.alert_msg = MonitorArguments.LOW_SPEED

            elif sent_rate > high_limit or recv_rate > high_limit:
                self.alert_msg = MonitorArguments.HIGH_SPEED

            else:
                self.alert_msg = MonitorArguments.SPEED_OK

            self.logger.logger.info(self.alert_msg)

        except Exception as err:
            self.logger.logger.error(err)
            raise MonitorError(f"Error while alerting user: {err}")

    def plot_graph(self, show_graphs: bool) -> None:
        """
        This function creates a connection rate graph and shows it if "show_graphs" is true.
        :param show_graphs: A boolean variable. True to show, False otherwise.
        :return: None
        """
        try:

            plt.plot(self.sent_rates, label=MonitorArguments.UPLOAD)
            plt.plot(self.recv_rates, label=MonitorArguments.DOWNLOAD)

            plt.xlabel(MonitorArguments.XLABEL)
            plt.ylabel(MonitorArguments.YLABEL)
            title = plt.title(self.alert_msg)
            title.set_color((MonitorArguments.PINK))
            plt.legend()
            plt.grid(True)
            plt.get_current_fig_manager().set_window_title(self.__class__.__name__)

            if show_graphs:
                plt.show(block=False)
                plt.pause(MonitorArguments.PAUSE_TIME_DEFAULT)
                plt.close()

        except Exception as err:
            self.logger.logger.error(err)
            raise GraphError(f"Error while creating a connection rate graph: {err}")

    def save_graph(self, save_graph: bool) -> None:
        """
        This function saves the graphs if "save_graphs" is true.
        :param save_graph: A boolean variable. True to save, False otherwise.
        :return: None
        """
        if save_graph:
            try:
                graph_name = path.join(MonitorArguments.GRAPHS, MonitorArguments.GRAPH_NAME)
                plt.savefig(graph_name)

            except Exception as err:
                self.logger.logger.error(err)
                raise GraphError(f"Unable to save the graph: {err}")

    def handle_monitor(self, dev_mode: bool, sent_rate: float, recv_rate: float, interface_status: bool, show_graphs: bool,
                       save_graphs: bool) -> None:
        """
        This function handles the monitor.
        :param dev_mode: A boolean variable. True to show the logs in the terminal, False otherwise.
        :param sent_rate: The current upload.
        :param recv_rate: The current download.
        :param interface_status: A boolean variable. True if the running interface is up, False if down.
        :param show_graphs: A boolean variable. True to show the graphs, False otherwise.
        :param save_graphs: A boolean variable. True to save the graphs. False otherwise.
        :return: None
        """
        try:
            output = (f"{MonitorArguments.UPLOAD}: {sent_rate:.2f} {MonitorArguments.MBPS} |"
                      f" {MonitorArguments.DOWNLOAD} : {recv_rate:.2f} {MonitorArguments.MBPS}")
            self.logger.logger.info(output)
            self.alert_user(sent_rate, recv_rate, MonitorArguments.low_limit, MonitorArguments.high_limit,
                            interface_status)

            # Development mode: This mode enables to get the alerts in the terminal in order to debug.
            if dev_mode:
                print(output)
                if self.alert_msg is not None:
                    print(self.alert_msg)

            self.plot_graph(show_graphs)
            self.save_graph(save_graphs)

        except Exception as err:
            self.logger.logger.error(err)
            raise MonitorError(f"Unable to handle {self.__class__.__name__}, Error: {err}")

    def run(self) -> None:
        """
        This function runs all the methods that mention above.
        :return: None
        """
        interface_name = self.network.get_running_interface()

        # fetch needed configs
        dev_mode = MonitorArguments.dev_mode
        show_graphs = MonitorArguments.show_graphs
        save_graphs = MonitorArguments.save_graph
        time_interval = MonitorArguments.time_interval

        # Create graphs directory
        self.functions.create_dir(MonitorArguments.GRAPHS)

        try:
            while True:
                self.sent_rates.clear()
                self.recv_rates.clear()

                interface_status = self.network.validate_running_interface_status(interface_name)
                self.calculate_connection_rate_speedtest(time_interval)

                if self.sent_rates and self.recv_rates:
                    sent_rate = self.sent_rates[MonitorArguments.FIRST_DATA]
                    recv_rate = self.recv_rates[MonitorArguments.FIRST_DATA]
                else:
                    sent_rate = MonitorArguments.FIRST_DATA
                    recv_rate = MonitorArguments.FIRST_DATA
                self.handle_monitor(dev_mode, sent_rate, recv_rate, interface_status, show_graphs, save_graphs)

        except Exception as err:
            self.logger.logger.error(err)
            raise MonitorError(f"Unable to run {self.__class__.__name__}, Error: {err}")


class MonitorArguments:
    fun = Functions()
    fun_arg = FunctionsArguments()

    JSON_DATA = fun.get_data_json(fun_arg.CONFIG_JSON_PATH)

    # the parameters from the config.json file
    low_limit = float(JSON_DATA[fun_arg.LOW_LIMIT])
    high_limit = float(JSON_DATA[fun_arg.HIGH_LIMIT])
    time_interval = int(JSON_DATA[fun_arg.TIME_INTERVAL])
    show_graphs = fun.set_config_mode(str(JSON_DATA[fun_arg.SHOW_GRAPHS]))
    save_graph = fun.set_config_mode(str(JSON_DATA[fun_arg.SAVE_GRAPHS]))
    dev_mode = fun.set_config_mode(str(JSON_DATA[fun_arg.DEV_MODE]))

    # alert
    INTERFACE_DOWN = "ALERT: Interface is down!!!"
    LOW_SPEED = "ALERT: Low Internet Speed Detected"
    HIGH_SPEED = "ALERT: High Internet Speed Detected"
    SPEED_OK = "ALERT: Speed is OK"

    # date
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATE_NOW = datetime.datetime.now().strftime(DATE_FORMAT)
    ONE_MINUTE_IN_SECONDS = 60

    # graph
    UPLOAD = "Upload"
    DOWNLOAD = "Download"
    TIME = "Time"
    XLABEL = f'{TIME} : {DATE_NOW}'
    YLABEL = "Connection Rate (Mbps)"
    GRAPHS = "/home/dev/PycharmProjects/NetMonitorr/Graphs"
    PAUSE_TIME_DEFAULT = 3
    GRAPH_NAME = f"connection_rate_{DATE_NOW}.png"
    PINK = 1, 0, 0.5

    # speedtest
    THREADS_DEFAULT = 4
    CONVERSION_NUMBER = 8
    MBPS = "Mbps"

    FIRST_DATA = 0


class MonitorError(Exception):
    pass


class SpeedTestError(Exception):
    pass


class GraphError(Exception):
    pass
