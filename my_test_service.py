import sys
import time

import servicemanager  # noqa; for logging
import win32service
import win32serviceutil  # for `ServiceFramework` and command line helper


class MyTestService:
    running: bool

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            time.sleep(30)
            servicemanager.LogInfoMsg("My Test Service is running!")
            time.sleep(30)
            servicemanager.LogErrorMsg("My Test Service is running!")
            time.sleep(30)
            servicemanager.LogWarningMsg("My Test Service is running!")


class MyServiceFramework(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MyTestService'
    _svc_display_name_ = 'My Test Service'
    service_impl: MyTestService

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = MyTestService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.service_impl.run()


def set_service_config():
    """
    Adjust service startup type and recovery actions using direct win32service calls.
    This bypasses the older 'win32serviceutil.ChangeServiceConfig2' which may not exist.
    """
    service_name = 'MyTestService'

    # Open the Service Control Manager
    scm_handle = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    if not scm_handle:
        raise RuntimeError("Could not open SCM")

    try:
        # Open the specific service
        service_handle = win32service.OpenService(
            scm_handle,
            service_name,
            win32service.SERVICE_ALL_ACCESS
        )
        if not service_handle:
            raise RuntimeError(f"Could not open service {service_name}")

        try:
            # 1) Set startup type to 'Automatic'
            #
            #   ChangeServiceConfig signature:
            #     (hService,
            #      ServiceType,
            #      StartType,
            #      ErrorControl,
            #      BinaryPathName,
            #      LoadOrderGroup,
            #      TagId,
            #      Dependencies,
            #      ServiceStartName,
            #      Password,
            #      DisplayName)
            #
            #   Using None or 0 for parameters we don't want to change.
            #
            win32service.ChangeServiceConfig(
                service_handle,
                win32service.SERVICE_NO_CHANGE,  # ServiceType (unchanged)
                win32service.SERVICE_AUTO_START,  # StartType -> Automatic
                win32service.SERVICE_ERROR_NORMAL,  # ErrorControl
                None,  # BinaryPathName
                None,  # LoadOrderGroup
                False,  # TagId
                None,  # Dependencies
                None,  # ServiceStartName
                None,  # Password
                None  # DisplayName
            )

            # 2) Configure recovery actions via ChangeServiceConfig2
            #
            #    Each action is a tuple: (ActionType, DelayInMilliseconds)
            #    For example, SC_ACTION_RESTART = 1
            #
            failure_actions = {
                'ResetPeriod': 0,  # 0 = never reset the failure count
                'RebootMsg': '',  # Only relevant if an action is reboot
                'Command': '',  # Program to run on failure (optional)
                'Actions': [
                    (win32service.SC_ACTION_RESTART, 300000),  # 1st failure (5 min)
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
            win32service.CloseServiceHandle(service_handle)
    finally:
        win32service.CloseServiceHandle(scm_handle)


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyServiceFramework)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # This handles: install, remove, start, stop, etc.
        win32serviceutil.HandleCommandLine(MyServiceFramework)

        # After "install", call set_service_config() to set Auto-Start & Recovery
        if 'install' in sys.argv:
            set_service_config()


if __name__ == '__main__':
    init()
