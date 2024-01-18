@echo off
tasklist|find /i "MAA.exe"
if %errorlevel%==0 ( 
taskkill /f /t /im  MAA.exe
) else (
	echo "exit"
)
EXIT