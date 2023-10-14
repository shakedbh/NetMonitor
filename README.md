# NetMonitor
NetMonitor is an automation that monitors the connection rate.

This automation written in Python 3.8  with PyCharm on Ubuntu 20.04.

## Usage:
``` $ sudo cp <project_directory_path>/netmonitor.service  /etc/systemd/system/netmonitor.service ```

``` $ sudo systemctl daemon-reload ```

``` $ sudo systemctl enable netmonitor.service ```

``` $ sudo systemctl start netmonitor.service ```

To check the status:

``` $ sudo systemctl status netmonitor.service ```
