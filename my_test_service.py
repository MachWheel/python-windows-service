"""
Sample Windows Service using `PyWin32`.

This service demonstrates:
  - How to create a basic Windows Service in Python
  - How to log messages at intervals
  - How to configure Automatic startup and Recovery (auto-restart)

See `README.md` for more details.
"""

import sys
import time

import servicemanager  # noqa; For logging to the Windows Event Viewer
import win32service
import win32serviceutil  # For the ServiceFramework and command-line helper


class MyTestService:
    """
    -> Modify the 'run' method to implement your service
    """

    running: bool

    def stop(self):
        """Stop the service by setting 'running' to False."""
        self.running = False

    def run(self):
        """
        The main loop of the service. Logs messages at intervals.
        -> Tweak time.sleep() or log calls as needed to change behavior.
        """
        self.running = True
        while self.running:
            # [your service logic goes here]
            time.sleep(30)
            servicemanager.LogInfoMsg("My Test Service is running!")
            time.sleep(30)
            servicemanager.LogErrorMsg("My Test Service is running!")
            time.sleep(30)
            servicemanager.LogWarningMsg("My Test Service is running!")


class MyServiceFramework(win32serviceutil.ServiceFramework):
    """
    Core Windows Service class that ties your Python logic to the Windows SCM.

    The attributes below specify how Windows sees your service:
      - _svc_name_: internal name (no spaces) used by the OS
      - _svc_display_name_: service name shown in 'services.msc'
    """

    _svc_name_ = 'MyTestService'
    _svc_display_name_ = 'My Test Service'
    service_impl: MyTestService

    def SvcStop(self):
        """
        Called by Windows when the service is asked to stop.
        We let Windows know we're stopping, then call 'stop' on our service_impl.
        """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """
        Called by Windows when the service starts.
        We prepare our 'MyTestService' and start its main loop.
        """
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = MyTestService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.service_impl.run()


def set_service_config():
    """
    Adjust service startup type and recovery actions using direct PyWin32 calls.

    -> Where to tweak startup type:
       `win32service.ChangeServiceConfig` call below sets
       SERVICE_AUTO_START (Automatic). If you need manual start, change to
       SERVICE_DEMAND_START, etc.

    -> Where to tweak failure/recovery actions:
       The 'failure_actions' dictionary sets how the service recovers.
       By default, it automatically restarts the service after 5 minutes
       on first, second, and subsequent failures.
       Change the (ActionType, Delay) tuples or 'ResetPeriod' to suit your needs.
    """
    service_name = 'MyTestService'

    # Open the Service Control Manager
    scm_handle = win32service.OpenSCManager(
        None,  # local machine
        None,  # ServicesActive database
        win32service.SC_MANAGER_ALL_ACCESS
    )
    if not scm_handle:
        raise RuntimeError("Could not open SCM (Service Control Manager)")

    try:
        # Open the specified service by name
        service_handle = win32service.OpenService(
            scm_handle,
            service_name,
            win32service.SERVICE_ALL_ACCESS
        )
        if not service_handle:
            raise RuntimeError(f"Could not open service {service_name}")

        try:
            # 1) Set startup type to Automatic
            win32service.ChangeServiceConfig(
                service_handle,
                win32service.SERVICE_NO_CHANGE,    # Keep service type as is
                win32service.SERVICE_AUTO_START,   # Automatic start
                win32service.SERVICE_ERROR_NORMAL, # Error control
                None,  # Path to the service binary (unchanged)
                None,  # Load order group
                False, # Tag ID
                None,  # Dependencies
                None,  # Service start name
                None,  # Password
                None   # Display name
            )

            # 2) Configure recovery actions
            #    Each tuple is (ActionType, DelayInMilliseconds).
            #    SC_ACTION_RESTART = 1 => restart the service
            failure_actions = {
                'ResetPeriod': 0,   # 0 => never reset the failure count
                'RebootMsg': '',    # Only used if SC_ACTION_REBOOT
                'Command': '',      # Only used if SC_ACTION_RUN_COMMAND
                'Actions': [
                    (win32service.SC_ACTION_RESTART, 300000),  # 1st failure
                    (win32service.SC_ACTION_RESTART, 300000),  # 2nd failure
                    (win32service.SC_ACTION_RESTART, 300000),  # Subsequent
                ]
            }

            win32service.ChangeServiceConfig2(
                service_handle,
                win32service.SERVICE_CONFIG_FAILURE_ACTIONS,
                failure_actions
            )
        finally:
            # Always close the service handle
            win32service.CloseServiceHandle(service_handle)
    finally:
        # Always close the SCM handle
        win32service.CloseServiceHandle(scm_handle)


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
        servicemanager.PrepareToHostSingle(MyServiceFramework)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # Installing, removing, starting, stopping, etc.
        win32serviceutil.HandleCommandLine(MyServiceFramework)

        # If the user installed the service, configure startup type & recovery
        if 'install' in sys.argv:
            set_service_config()


if __name__ == '__main__':
    init()
