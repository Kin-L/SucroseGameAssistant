@echo off
tasklist|find /i "SGA.exe"
if %errorlevel%==0 ( 
 echo "exit"
) else (
start /d "D:\Kin-project\sga_sucrose_game_assistant" SGA.exe
)
@echo on