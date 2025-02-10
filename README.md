# 1. Setup
Use Python 3.9 to avoid `pywin32` known bugs:
```
py -m pip install virtualenv
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

# 2. Build 
- As one `.exe` file: *will run as two processes*
```
pyinstaller --onefile --runtime-tmpdir=. --hidden-import win32timezone main.py --name my-service
```

- As one folder: *will run as one process*
```
pyinstaller --runtime-tmpdir=. --hidden-import win32timezone main.py --name my-service
```

# 3. Install and start the service:
Place `_bat_scripts/install_service.bat` in the same folder as the generated `.exe` then double click it.

# 4. Stop and remove the service:
Place `_bat_scripts/remove_service.bat` in the same folder as the generated `.exe` then double click it.

# Service commands *(run as admin)*
- Install:
```
my-service.exe install
```

- Start:
```
my-service.exe start
```

- Stop:
```
my-service.exe stop
```

- Uninstall:
```
my-service.exe remove
```

- Debug:
```
my-service.exe debug
```
