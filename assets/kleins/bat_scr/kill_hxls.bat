@echo off
tasklist|find /i "环行旅舍.exe"
if %errorlevel%==0 ( 
 taskkill /f /t /im  环行旅舍.exe
) else (
	echo "exit"
)
@echo on