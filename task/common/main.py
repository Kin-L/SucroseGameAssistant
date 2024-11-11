from ..default_task import Task
from tools.environment import *
from traceback import format_exc
import subprocess
import ctypes
import win32gui
import win32process
import psutil
IsWindowVisible = ctypes.windll.user32.IsWindowVisible


def find_hwnd_from_pid(_pid):
    def callback(_hwnd, _hwnds):
        # if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)

        if found_pid == _pid:
            _hwnds.append(hwnd)
        return True

    _hwnds = []
    win32gui.EnumWindows(callback, _hwnds)
    for hwnd in _hwnds:
        if IsWindowVisible(hwnd):
            return hwnd


def find_pid_from_name(_name):
    for proc in psutil.process_iter():
        if _name in proc.name():
            return proc.pid


class TaskCommon(Task):
    def __init__(self):
        super().__init__()
        self.proc = None
        self.hwnd = 0
        self.pid = 0
        self.fram = (0, 0, 0, 0)

    def common_start(self, task: type[dir]):
        _k = False
        self.task = task
        self.indicate("开始任务:通用执行")
        env.mode(2)
        # noinspection PyBroadException
        try:
            # 启动流程
            _p = task["启动路径"]
            _c = task["附加命令"]
            self.proc = subprocess.Popen(f"start \"\" \"{_p}\" {_c}", shell=True)
            self.pid = self.proc.pid
            self.hwnd = find_hwnd_from_pid(self.proc.pid)
            self.fram = win32gui.GetWindowRect(self.hwnd)

            # 开始流程
            wait(task["开始前等待时间"])
            env.OCR.enable()
            if task["启动操作类型"] == 0:
                pass
            elif task["启动操作类型"] == 3:
                add_press(task["启动操作内容"])
            else:
                if task["启动判断进程名"]:
                    pid = find_pid_from_name(task["启动判断进程名"])
                else:
                    pid = self.pid
                hwnd = find_hwnd_from_pid(pid)
                fram = win32gui.GetWindowRect(hwnd)
                if task["启动判断指定区域"]:
                    (x1, y1, x2, y2) = task["启动判断指定区域"]
                    zone = (fram[0]+x1, fram[1]+y1, fram[0]+x2, fram[1]+y2)
                else:
                    zone = "ALL"
                if task["启动操作类型"] == 1:
                    try:
                        pos = wait_text(task["启动操作内容"], zone)
                    except Exception:
                        self.indicate("未识别到目标文本")
                        raise RuntimeError("通用执行:未识别到目标文本")
                    click(pos)
                elif task["启动操作类型"] == 2:
                    try:
                        pos = wait_pic(task["启动操作内容"], zone)
                    except Exception:
                        self.indicate("未识别到目标图像")
                        raise RuntimeError("通用执行:未识别到目标图像")
                    click(pos)
            wait(task["开始后等待时间"])

            # 结束流程
            if task["结束判断进程名"]:
                pid = find_pid_from_name(task["结束判断进程名"])
            else:
                pid = self.pid
            proc = psutil.Process(pid)
            num, sec = task["判断循环"]
            if task["结束判断类型"] == 0:
                while 1:
                    if proc.is_running():
                        wait(5000)
            else:
                if task["结束判断类型"] == 3:
                    n = 0
                    while 1:
                        if proc.cpu_percent(0.1) > task["结束判断内容"]:
                            wait(5000)
                        else:
                            if n < num:
                                n += 1
                                sleep(sec)
                            else:
                                break
                else:
                    hwnd = find_hwnd_from_pid(pid)
                    fram = win32gui.GetWindowRect(hwnd)
                    if task["结束判断指定区域"]:
                        (x1, y1, x2, y2) = task["结束判断指定区域"]
                        zone = (fram[0] + x1, fram[1] + y1, fram[0] + x2, fram[1] + y2)
                    else:
                        zone = "ALL"
                    if task["结束判断类型"] == 1:
                        n = 0
                        while 1:
                            if not find_text(task["结束判断内容"], zone):
                                wait(5000)
                            else:
                                if n < num:
                                    n += 1
                                    sleep(sec)
                                else:
                                    break
                    elif task["结束判断类型"] == 2:
                        n = 0
                        while 1:
                            if not find_pic(task["结束判断内容"], zone)[0]:
                                wait(5000)
                            else:
                                if n < num:
                                    n += 1
                                    sleep(sec)
                                else:
                                    break
            # 关闭进程

        except Exception:
            self.indicate("任务执行异常:通用执行", log=False)
            logger.error("任务执行异常:通用执行\n%s" % format_exc())
            _k = True
        env.mode(0)
        self.indicate("完成任务:通用执行")
        return _k


if __name__ == '__main__':
    pass
