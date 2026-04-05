@echo off
py -m pip install pyinstaller
py -m PyInstaller --onefile --windowed main.py --name PortMonitorDemo
pause