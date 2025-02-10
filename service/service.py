import time

import servicemanager  # noqa


class MyService:
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
            # [YOUR LOGIC GOES HERE]
            time.sleep(30)
            servicemanager.LogInfoMsg("My Test Service is running!")
            time.sleep(30)
            servicemanager.LogErrorMsg("My Test Service is running!")
            time.sleep(30)
            servicemanager.LogWarningMsg("My Test Service is running!")
