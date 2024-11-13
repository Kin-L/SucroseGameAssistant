from os import kill
from os.path import isfile, split
from time import sleep
from win32con import PROCESS_ALL_ACCESS, SW_RESTORE
from win32gui import (FindWindow, EnumWindows, GetClassName, GetWindowText,
                      GetClientRect, ClientToScreen, IsIconic, ShowWindow, SetForegroundWindow, GetForegroundWindow)
from psutil import process_iter
from signal import SIGTERM
from subprocess import run


# 从exe名称获取pid
def get_pid(name):
    pids = process_iter()
    for pid in pids:
        # noinspection PyBroadException
        try:
            _name = pid.name()
            _pid = pid.pid
        except Exception:
            continue
        if _name == name:
            return _pid


# 正常关闭进程
def close(pid, sig=SIGTERM):
    kill(pid, sig)


# 获取进程pid及路径
def get_process_name(hwnd):
    from win32process import GetWindowThreadProcessId, GetModuleFileNameEx
    from win32api import OpenProcess
    pid = GetWindowThreadProcessId(hwnd)[1]
    mypy_proc = OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    path = GetModuleFileNameEx(mypy_proc, 0)
    return pid, path


# 根据类/标题查找窗口句柄
def find_hwnd(mode_cls_tit):
    mode, cls, tit = mode_cls_tit
    if mode:
        return FindWindow(cls, tit)
    else:
        hwnd_list = []
        EnumWindows(lambda _hwnd, _hwnd_list: _hwnd_list.append(_hwnd), hwnd_list)
        for hwnd in hwnd_list:
            try:
                class_name = GetClassName(hwnd)
                title = GetWindowText(hwnd)
                if cls in class_name and tit in title:
                    return hwnd
            except Exception as e:
                print(e)


class Software:
    def __init__(self, compile_resolution):
        self.compile_resolution = compile_resolution
        self.path, self.dir, self.name = None, None, None
        self.pid, self.hwnd = None, None
        self.mode_cls_tit = None
        self.frame, self.wide, self.high, self.zoom = None, None, None, None

    def set_path(self, path: str):
        if isfile(path):
            self.path, [self.dir, self.name] = path, split(path)
            return True
        else:
            print("error:Software 无效路径。")
            return False

    def set_pid(self, hwnd):
        if hwnd:
            self.pid, self.path = get_process_name(hwnd)
            self.dir, self.name = split(self.path)
        else:
            print("error:Software 窗口未启动。")

    def set_hwnd_find(self, mode, cls, tit):
        if mode == 0:  # 精确设置
            self.mode_cls_tit = [True, cls, tit]
        elif mode == 1:
            self.mode_cls_tit = [False, cls, tit]
        elif mode == 2:  # 通过路径设置
            if self.path is not None:
                if self.name == "YuanShen.exe":
                    self.mode_cls_tit = [True, "UnityWndClass", "原神"]
                elif self.name == "环行旅舍.exe":
                    self.mode_cls_tit = [True, "UnityWndClass", "环行旅舍"]
                elif self.name == "MAA.exe":
                    self.mode_cls_tit = [False, "HwndWrapper[MAA.exe", "MAA"]
                elif self.name == "March7th Assistant.exe":
                    self.mode_cls_tit = [True, "ConsoleWindowClass", ""]
                else:
                    print("error:Software 不支持自动识别的软件。")
            else:
                print("error:Software 无效路径。")

    def run(self, second=30, num=2, fls=True, tit=None):
        if self.path is None:
            print("error:Software 需要先设置启动路径。")
            return 0
        else:
            self.hwnd = find_hwnd(self.mode_cls_tit)
            if self.hwnd:
                self.set_pid(self.hwnd)
                return 1
            else:
                if tit is None:
                    cmd = f"start \"\" \"{self.path}\""
                else:
                    cmd = f"start \"{tit}\" \"{self.path}\""
                if fls:
                    cmd = cmd + " -popupwindow"
                for n in range(num):
                    run(cmd, shell=True)
                    # run("start /d \"" + self.dir + "\" " + self.name + " -popupwindow", shell=True)
                    for i in range(second):
                        sleep(1)
                        self.hwnd = find_hwnd(self.mode_cls_tit)
                        if self.hwnd:
                            self.set_pid(self.hwnd)
                            print("软件启动成功。")
                            return 2
                print(f"error:启动超时。({second*num}s)")
                return 0

    def isalive(self):
        return find_hwnd(self.mode_cls_tit)

    def find_hwnd(self):
        self.hwnd = find_hwnd(self.mode_cls_tit)
        return self.hwnd

    def kill(self, second=10, num=2):
        if self.hwnd:
            for n in range(num):
                close(self.pid)
                for i in range(second):
                    sleep(1)
                    self.hwnd = find_hwnd(self.mode_cls_tit)
                    if not self.hwnd:
                        print("软件关闭成功。")
                        return True
            print(f"error:关闭超时。({second*num}s)")
            return False
        else:
            print("该软件未启动。")

    def get_window_information(self, mode=True):
        if self.hwnd:
            # f = GetWindowRect(self.hwnd)
            (p1, p2, w, h) = GetClientRect(self.hwnd)
            x1, y1 = ClientToScreen(self.hwnd, (0, 0))
            if not mode:
                x_zoom, y_zoom = w / self.compile_resolution[0], h / self.compile_resolution[1]
                self.zoom = min(x_zoom, y_zoom)
                self.frame, self.wide, self.high = (x1, y1, x1 + w, y1 + h), w, h
                return True
            elif (1.7 <= round(w / h, 3) <= 1.8) and (664 <= h <= 2160) and mode:
                x_zoom, y_zoom = w / self.compile_resolution[0], h / self.compile_resolution[1]
                self.zoom = min(x_zoom, y_zoom)
                self.frame, self.wide, self.high = (x1, y1, x1+w, y1+h), w, h
                return True
            else:
                print(f"不适配的分辨率: {self.wide} × {self.high}")
                self.zoom = None
                return False

        else:
            print("error:软件还未启动。")
            return False

    def isforeground(self):
        current_hwnd = GetForegroundWindow()
        if current_hwnd == self.hwnd:
            return True
        else:
            return False

    def foreground(self):
        for i in range(10):
            current_hwnd = GetForegroundWindow()
            if current_hwnd == self.hwnd:
                return True
            if IsIconic(self.hwnd):
                ShowWindow(self.hwnd, SW_RESTORE)
                sleep(0.2)
            if current_hwnd != self.hwnd:
                SetForegroundWindow(self.hwnd)
                sleep(0.2)
        return False
