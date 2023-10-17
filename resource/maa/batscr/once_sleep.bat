@echo off 
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
D:
cd D:\Kin-project\python-SGA
if exist cache\once_sleep_flag.txt set if=Ture
if "%if%"=="Ture" (
Rem 5秒后电脑睡眠。
del cache\once_sleep_flag.txt
powercfg -h off
TIMEOUT /T 5
rundll32.exe powrprof.dll,SetSuspendState 0,1,0
powercfg -h on
) else (
Rem "无操作"
)
echo