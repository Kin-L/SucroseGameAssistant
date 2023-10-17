# -*- coding:gbk -*-
import os,datetime
from subprocess import run
from function import *
from PyQt5.QtCore import  QThread,pyqtSignal
import sys,json,shutil
# pyinstaller -D -w D:\Kin-project\python\venv\maa\maa.py
class Thread_maa(QThread):
    testsignal = pyqtSignal(str)
    accomplish = pyqtSignal(int)
    def __init__(self,tlist):
        super(Thread_maa, self).__init__()
        self.tlist =tlist

    def run(self):
        print(self.tlist)
        self.cmdrun("start "" /d resource\maa\\batscr C:\Windows\System32\wscript.exe kill-MAA.vbs")
        self.testsignal.emit("(重新）启动MAA。")
        wait(3000)
        gui_path = os.path.split(self.tlist[0][0])[0] + "\config\gui.json"
        with open(gui_path, 'r', encoding='utf-8') as g:
            self.maagui = json.load(g)
        setcurrent = self.tlist[0][1]
        import copy
        config_SGA = copy.deepcopy(self.maagui["Configurations"][setcurrent])
        if not setcurrent in list(self.maagui["Configurations"].keys()):
            self.testsignal.emit("error：无效配置。")
            self.accomplish.emit(3)
        else:
            if self.tlist[1][2]:
                if not os.path.exists("cache\once_sleep_flag.txt"):
                    f = open(r"cache\once_sleep_flag.txt", 'w', encoding='utf-8')
                    f.close()
                endscr = os.getcwd() + "\\resource\maa\\batscr\once_sleep.bat"
            else:endscr = ""
            config_SGA["Start.EndsWithScript"] = endscr
            if self.tlist[1][0]:
                AfterCompleted = "ExitEmulator"
            else:
                AfterCompleted = "DoNothing"
            config_SGA["MainFunction.ActionAfterCompleted"] = AfterCompleted
            self.maagui["Configurations"]["SGA-cache"] = config_SGA
            self.maagui["Global"]["Timer.Timer8"] = True
            self.maagui["Global"]["Timer.Timer8.Config"] = "SGA-cache"
            (HH,mm)=(datetime.datetime.now()+datetime.timedelta(minutes=3)).timetuple()[3:5]
            self.maagui["Global"]["Timer.Timer8Hour"] = HH
            self.maagui["Global"]["Timer.Timer8Min"] = mm
            self.maagui["Global"]["Timer.CustomConfig"] = True
            with open(gui_path, 'w', encoding='utf-8') as g:
                json.dump(self.maagui, g, ensure_ascii=False, indent=1)
            dir, file = os.path.split(self.tlist[0][0])
            self.cmdrun("start /d \"" + dir + "\" " + file)
            wait(5000)
            self.testsignal.emit("执行完成，MAA3分钟后自动开始运行。")
            if self.tlist[1][1]:
                self.cmdrun("taskkill /f /t /im  SGA.exe")
            self.accomplish.emit(1)
    def cmdrun(self,cmdstr):
        run(cmdstr, shell=True)
if __name__ == '__main__':pass






