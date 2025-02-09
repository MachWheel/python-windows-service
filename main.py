"""
Sample Windows Service using `pywin32`

This service demonstrates:
  - How to create a basic Windows Service in Python
  - How to log messages at intervals
  - How to configure Automatic startup and Recovery (auto-restart)

See `README.md` for more details.
"""

import sys

import servicemanager  # noqa; For logging to the Windows Event Viewer
import win32serviceutil  # For the ServiceFramework and command-line helper

from service_framework import WindowsService
from service_config import configure_service


def init():
    """
    Entry point for the script.
    - If called with no arguments, assume Windows is starting the service.
    - If called with arguments (install, start, stop, etc.), we pass them
      through to `win32serviceutil.HandleCommandLine`.

    After 'install', we invoke 'set_service_config' to finalize the
    startup type and failure actions for this service.
    """
    if len(sys.argv) == 1:
        # Running as a service
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WindowsService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # Installing, removing, starting, stopping, etc.
        win32serviceutil.HandleCommandLine(WindowsService)

        # If the user installed the service, configure startup type & recovery
        if 'install' in sys.argv:
            configure_service()


if __name__ == '__main__':
    init()
