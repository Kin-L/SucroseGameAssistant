@echo off Rem 5√Î∫ÛµÁƒ‘ÀØ√ﬂ°£
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
powercfg -h off
TIMEOUT /T 5
rundll32.exe powrprof.dll,SetSuspendState 0,1,0
powercfg -h on
EXIT
echo