from maincode.tools.myclass import SGAStop
from maincode.tools.main import GetWindow, logger, CmdRun

from time import sleep ,time
from win32gui import FindWindow
from os import path


def _check(self):
    for i in range(20):
        win = GetWindow("Python")
        if win is None:
            return True
        else:
            self.send(f"三月七或一条龙未关闭,即将关闭")
            win.close()
        sleep(0.5)
    self.send(f"关闭超时")
    return False

def _run(self):
    timeout = self.para["timeout"]*60
    start_time = int(time())
    path = self.para["path"]
    
    if path.isfile(_path):
        dire, name = path.split(path)
        if  "March7th" in name:
            _path = dire + "/March7th Assistant.exe"
        elif "OneDragon" in name:
            _path = dire + "/OneDragon Scheduler.exe"
        else:
            self.send("无效启动路径")
            raise ValueError("无效启动路径")
        if not path.isfile(_path):
            self.send("无效启动路径")
            raise ValueError("无效启动路径")
    else:
        self.send("无效启动路径")
        raise ValueError("无效启动路径")
        
    cmd = f"start \"\" \"{_path}\""
    for i in range(2):
        CmdRun(cmd)
        sleep(60)
        win = GetWindow("崩坏：星穹铁道")
        if win is not None:
            break
    if timeout == 0:
        while 1:
            win = GetWindow("崩坏：星穹铁道")
            if win is None:
                return True
            sleep(20)
    else:
        while start_time - int(time()) < timeout:
            sleep(20)
        win = GetWindow("崩坏：星穹铁道")
        win2 = GetWindow("Python")
        win.close()
        win2.close()
        self.send("超时时间到，关闭崩坏：星穹铁道")
        return True

def taskstart(self):
    self.send("开始任务:崩坏：星穹铁道", True)
    if not _check(self):
        return False
    if _run(self):
        self.send("崩坏：星穹铁道任务已完成")
    else:
        self.send("崩坏：星穹铁道任务异常")
        return False
    return True



