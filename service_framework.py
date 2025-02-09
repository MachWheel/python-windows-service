import win32service
import win32serviceutil

from service import MyService


class WindowsService(win32serviceutil.ServiceFramework):
    """
    Core Windows Service class that ties your Python logic to the Windows SCM.

    The attributes below specify how Windows sees your service:
      - _svc_name_: internal name (no spaces) used by the OS
      - _svc_display_name_: service name shown in 'services.msc'
    """

    _svc_name_ = 'MyService'
    _svc_display_name_ = 'My Service'
    service_impl: MyService

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
        We prepare our 'MyService' and start its main loop.
        """
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = MyService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.service_impl.run()
