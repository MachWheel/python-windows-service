# 1. Setup
Use Python 3.9 to avoid `pywin32` known bugs:
```
py -m pip install virtualenv
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

# 2. Build
```
pyinstaller --onefile --runtime-tmpdir=. --hidden-import win32timezone main.py --name my-service
```

# 3. Run as administrator

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
