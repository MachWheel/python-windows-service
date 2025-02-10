import win32service


def configure_service():
    """
    Adjust service startup type and recovery actions using direct PyWin32 calls.

    -> Where to tweak startup type:
       `win32service.ChangeServiceConfig` call below sets
       SERVICE_AUTO_START (Automatic). If you need manual start, change to
       SERVICE_DEMAND_START, etc.

    -> Where to tweak failure/recovery actions:
       The 'failure_actions' dictionary sets how the service recovers.
       By default, it automatically restarts the service after 1 minute
       on first, second, and subsequent failures.
       Change the (ActionType, Delay) tuples or 'ResetPeriod' to suit your needs.
    """
    service_name = 'MyService'

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
                    (win32service.SC_ACTION_RESTART, 60000),  # 1st failure
                    (win32service.SC_ACTION_RESTART, 60000),  # 2nd failure
                    (win32service.SC_ACTION_RESTART, 60000),  # Subsequent
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
