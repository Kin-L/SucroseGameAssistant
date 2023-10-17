@echo off
tasklist|find /i "SGA.exe"
if %errorlevel%==0 ( 
 taskkill /f /t /im  SGA.exe
) else (
	echo "exit"
)
@echo on