# Prerequisites:
```pip3 install pywin32 pyinstaller```

# Build:
```pyinstaller --onefile --runtime-tmpdir=. --hidden-import win32timezone my_test_service.py```

# With Administrator privilges
# Install:
```my_test_service.exe install```

# Start:
```my_test_service.exe start```

# Install with autostart:
```my_test_service.exe --startup delayed install```

# Debug:
```my_test_service.exe debug```

# Stop:
```my_test_service.exe stop```

# Uninstall:
```my_test_service.exe remove```
