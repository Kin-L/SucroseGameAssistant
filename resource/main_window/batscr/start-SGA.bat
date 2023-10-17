@echo off
tasklist|find /i "SGA.exe"
if %errorlevel%==0 ( 
 echo "exit"
) else (
start /d "D:\Kin-project\python-SGA" SGA.exe
)
@echo on