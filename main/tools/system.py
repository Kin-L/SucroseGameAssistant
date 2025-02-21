from subprocess import run as cmd_run
from psutil import process_iter
from win10toast import ToastNotifier
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER, windll
from comtypes import CLSCTX_ALL


# 从exe名称获取pid
def get_pid(name):
    for proc in process_iter():
        # noinspection PyBroadException
        try:
            if proc.name() == name:
                return proc.pid
        except Exception:
            continue
    return 0


# 关闭进程
def close(_v):
    if isinstance(_v, int):
        # 根据pid杀死进程
        process = 'taskill /f /pid %s' % _v
        cmd_run(process)
    elif isinstance(_v, str):
        # 根据进程名杀死进程
        pro = 'taskill /f /im %s' % _v
        cmd_run(pro)
    else:
        raise ValueError(f"close异常传输值：{_v}")


# windows提示
def notify(title, massage):
    toaster = ToastNotifier()
    toaster.show_toast(title,
                       massage,
                       icon_path="assets/main_window/ui/ico/SGA.ico",
                       duration=5,
                       threaded=True)


# 查询静音状态
def get_mute():
    # noinspection PyBroadException
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume.GetMute()
    except Exception:
        return 0


# 熄屏
def screen_off():
    power_off = 2
    windll.user32.PostMessageW(0xffff, 0x0112, 0xF170, power_off)
    shell32 = windll.LoadLibrary("shell32.dll")
    shell32.ShellExecuteW(None, 'open', 'rundll32.exe', 'USER32', '', 5)
