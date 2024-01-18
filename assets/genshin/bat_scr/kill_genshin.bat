@echo off
tasklist|find /i "YuanShen.exe"
if %errorlevel%==0 ( 
 taskkill /f /t /im  YuanShen.exe
) else (
	echo "exit"
)
@echo on