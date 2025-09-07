from maincode.tools.myclass import SGAStop
from maincode.tools.main import GetWindow, logger, CmdRun

from time import sleep ,time
from win32gui import FindWindow
from os import path


def onedragon_check(self):
    for i in range(20):
        win = GetWindow("Python")
        if win is None:
            return True
        else:
            self.send(f"一条龙未关闭,即将关闭")
            win.close()
        sleep(0.5)
    self.send(f"一条龙关闭超时")
    return False

def onedragon_run(self):
    timeout = self.para["timeout"]*60
    start_time = int(time())
    _path = self.para["path"]
    if not path.isfile(_path):
        self.send("无效启动路径")
        raise ValueError("无效启动路径")
    cmd = f"start \"\" \"{_path}\" -o"
    for i in range(2):
        CmdRun(cmd)
        sleep(60)
        win = GetWindow("绝区零")
        if win is not None:
            break
    if timeout == 0:
        while 1:
            win = GetWindow("绝区零")
            if win is None:
                return True
            sleep(20)
    else:
        while start_time - int(time()) < timeout:
            sleep(20)
        win = GetWindow("绝区零")
        win2 = GetWindow("Python")
        win.close()
        win2.close()
        self.send("超时时间到，关闭绝区零")
        return True

def taskstart(self):
    self.send("开始任务:绝区零", True)
    if not onedragon_check(self):
        return False
    if onedragon_run(self):
        self.send("绝区零任务已完成")
    else:
        self.send("绝区零任务异常")
        return False
    return True



