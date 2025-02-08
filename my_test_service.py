import sys
import time

import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging


class MyTestService:
    """Silly little application stub"""
    running: bool

    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        self.running = True
        while self.running:
            # To see the service log msgs:
            #   `Win + R`, then `eventvwr`
            time.sleep(30)
            servicemanager.LogInfoMsg("My Test Service is running!\nThis is an info msg.")
            time.sleep(30)
            servicemanager.LogErrorMsg("My Test Service is running!\nThis is an error msg.")
            time.sleep(30)
            servicemanager.LogWarningMsg("My Test Service is running!\nThis is a warning msg.")


class MyServiceFramework(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MyTestService'
    _svc_display_name_ = 'My Test Service'
    service_impl: MyTestService

    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """Start the service; does not return until stopped"""
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = MyTestService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # Run the service
        self.service_impl.run()


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyServiceFramework)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyServiceFramework)


if __name__ == '__main__':
    init()
