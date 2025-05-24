from subprocess import run as cmd_run
from psutil import process_iter
from win10toast import ToastNotifier
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER, windll
from comtypes import CLSCTX_ALL
from typing import Union
from win32api import MessageBox
import sys
from traceback import format_exc
from win32con import MB_OK, SW_RESTORE
from sgacode.tools.logger import Logger
from sgacode.tools.environment import Environment
from win32gui import (FindWindow, EnumWindows, GetClassName,
                      GetWindowText, IsIconic, ShowWindow,
                      SetForegroundWindow, GetForegroundWindow)
from pyuac import isUserAdmin
from time import sleep


# 从exe名称获取pid
def getpid(name: str) -> int:
    for proc in process_iter():
        # noinspection PyBroadException
        try:
            if proc.name() == name:
                return proc.pid
        except Exception:
            continue
    return 0


# 关闭进程
def killprocess(_process: Union[int, str]) -> None:
    if isinstance(_process, int):
        # 根据pid杀死进程
        cmd_run('taskill /f /pid %s' % _process)
    elif isinstance(_process, str):
        # 根据进程名杀死进程
        pro = 'taskill /f /im %s' % _process
        cmd_run(pro)
    else:
        raise ValueError(f"close异常传输值：{_process}")


# windows提示
def winnotify(title: str, massage: str) -> None:
    toaster = ToastNotifier()
    toaster.show_toast(title,
                       massage,
                       icon_path="assets/main_window/ui/ico/SGA.ico",
                       duration=5,
                       threaded=True)


# 查询静音状态
def getmute() -> bool:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMute()


# 熄屏
def screenoff() -> None:
    power_off = 2
    windll.user32.PostMessageW(0xffff, 0x0112, 0xF170, power_off)
    shell32 = windll.LoadLibrary("shell32.dll")
    shell32.ShellExecuteW(None, 'open', 'rundll32.exe', 'USER32', '', 5)


def gettracebackinfo(e) -> str:
    return str(e) + "\n" + format_exc()


def gettracebackvalue() -> (str, str):
    _, _, exc_traceback = sys.exc_info()
    frame = exc_traceback.tb_frame
    return frame.f_locals, frame.f_globals


def sendmessagebox(_str) -> None:
    MessageBox(0, _str, "砂糖代理", MB_OK)


def gethwnd(_mode: bool, _class: Union[str, None], _title: Union[str, None]) -> int:
    """
    :param _mode: 获取方法 True 精确查找 False 扫描
    :param _class: 类 str
    :param _title: 标题 str
    :return: 句柄 int 未找到时返回 0
    """
    if _mode:
        return FindWindow(_class, _title)
    else:
        if _class is None:
            _class = ""
        if _title is None:
            _title = ""
        hwnd_list = []
        EnumWindows(lambda _hwnd, _hwnd_list: _hwnd_list.append(_hwnd), hwnd_list)
        for hwnd in hwnd_list:
            # noinspection PyBroadException
            try:
                cls = GetClassName(hwnd)
                tit = GetWindowText(hwnd)
                if _class in cls and _title in tit:
                    return hwnd
            except Exception:
                continue
        return 0
    
    
def checkadmin():
    if not isUserAdmin():
        _str = "请手动使用管理员权限启动\n"\
               "可参考视频给予默认管理员权限启动：\n"\
               "https://www.bilibili.com/video/BV18kKAeYE2t"
        sendmessagebox(_str)
        exit(1)


def foreground(_hwnd: int) -> bool:
    if not _hwnd:
        return False
    for i in range(10):
        current_hwnd = GetForegroundWindow()
        if current_hwnd == _hwnd:
            return True
        if IsIconic(_hwnd):
            ShowWindow(_hwnd, SW_RESTORE)
            sleep(0.2)
        if current_hwnd != _hwnd:
            # noinspection PyBroadException
            try:
                SetForegroundWindow(_hwnd)
            except Exception:
                pass
            sleep(0.2)
    return False


def dictlisttype(_dict):
    return {key: type(key) for key, value in _dict.items()}


class ConfigTool(dict):
    def __init__(self, schema):
        super().__init__()
        self.schema = schema

    def getdefault(self):
        """
        根据schema规范生成默认字典
        :return: 包含默认值的字典
        """
        default_dict = {}
        for field, config in self.schema.items():
            if 'default' in config:
                default_dict[field] = config['default']
            elif config.get('required', True):
                # 为必填字段但没有默认值的字段生成默认值
                field_type = config.get('type')
                if field_type == str:
                    default_dict[field] = ""
                elif field_type == int:
                    default_dict[field] = 0
                elif field_type == float:
                    default_dict[field] = 0.0
                elif field_type == bool:
                    default_dict[field] = False
                elif field_type == list:
                    default_dict[field] = []
                elif field_type == dict:
                    default_dict[field] = {}
        return default_dict

    def init(self):
        super().__init__(self.getdefault())

    def check(self, data: dict):
        """
        验证字典是否符合规范
        :param data: 要验证的字典
        :return: (是否有效, 错误信息)
        """
        errors = []
        # 检查必填字段是否缺失
        for field, config in self.schema.items():
            if config.get('required', False) and field not in data:
                errors.append(f"缺少必填字段: {field}")
        # 检查字段类型
        for field, value in data.items():
            if field in self.schema:
                expected_type = self.schema[field].get('type')
                if expected_type and not isinstance(value, expected_type):
                    errors.append(f"字段 '{field}' 类型错误，应为 {expected_type}，实际为 {type(value)}")
        # 检查是否有未定义的字段
        for field in data:
            if field not in self.schema:
                errors.append(f"存在未定义的字段: {field}")
        return len(errors) == 0, errors


logger = Logger().getlogger()
env = Environment(logger)
if __name__ == '__main__':
    pass
