@echo off
tasklist|find /i "SGA.exe"
if %errorlevel%==0 ( 
 echo "exit"
) else (
start /d "D:\Kin-project\SucroseGameAssistant" SGA.exe True
)
@echo on