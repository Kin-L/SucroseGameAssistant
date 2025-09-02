import time
from maincode.tools.controller.operate import Operate
import winreg
from maincode.tools.main import logger
from ctypes import windll
from maincode.tools.main import GetWindow, CmdRun
from win32gui import FindWindow


class Controller(Operate):
    def __init__(self):
        self.SetLocal()
        super().__init__()
        self.window = None
        self.DeviceMode()

    def ChooseWindow(self, para, ref, max_retries=10, interval=0.5):  # title hwnd
        for _ in range(max_retries):
            self.window = GetWindow(para)
            if self.window is not None:
                break
            time.sleep(interval)
        else:
            raise ValueError("GetWindow 未获取到有效值")
        self.window.foreground()
        self.ChangeReference(ref)
        self.ChangeOperate(self.window.rect)
        logger.info(f"当前窗口：{self.window.rect}")

    @staticmethod
    def FindProgramPath(names, nametag="DisplayName", pathtag="DisplayIcon"):
        # 常见的注册表路径
        reg_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",  # 64位系统上的32位程序
        ]
        paths = []
        # 遍历注册表路径
        for reg_path in reg_paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        display_name = winreg.QueryValueEx(subkey, nametag)[0]
                        # print(display_name)
                        for name in names:
                            if name.lower() in display_name.lower():
                                print(display_name)
                                install_path = winreg.QueryValueEx(subkey, pathtag)[0]
                                if install_path:
                                    paths.append(install_path)
                    except (WindowsError, FileNotFoundError):
                        continue
            except WindowsError as e:
                logger.warning(f"无法访问注册表路径 {reg_path}: {e}")
                continue
        return list(paths)

    def SetLocal(self):
        user32 = windll.user32
        user32.SetProcessDPIAware()
        now_wid = user32.GetSystemMetrics(0)
        if now_wid == 0:
            raise RuntimeError("获取屏幕宽度失败")
        ori_wid = user32.GetSystemMetrics(0)
        ori_hig = user32.GetSystemMetrics(1)
        self.InitLocal((0, 0, ori_wid, ori_hig))
        self.scaling = round(ori_wid / now_wid, 2)

    def RunProg(self, _cmdline, _clsandtit, _wait):
        for _ in range(3):
            for _ in range(20):
                _list = [FindWindow(*item) for item in _clsandtit]
                for i in _list:
                    if i:
                        self.wait(_wait)
                        return i
                else:
                    CmdRun(_cmdline)
                    self.wait(0.5)
        return 0

    def DeviceMode(self, device="windows", exe_path=None):
        if device == "windows":
            self.__class__.screenshot = self.__class__.screenshot_win
        elif device == "emulator":
            self.exe_path = exe_path
            self.__class__.screenshot = self.__class__.screenshot_adb
            try:
                self.connect_to_emulator()
                self.WaitTime = (0, 10)
                h, w = self.getresolution()
                self.ChangeOperate((0, 0, w, h))
            except Exception as e:
                logger.error(f"连接模拟器失败: {e}")
                raise


if __name__ == '__main__':
    from maincode.config.info import info
    info.OcrPath = r"D:/Program Files (Green)/SGAv3/ocr-json/PaddleOCR-json.exe"

ctler = Controller()
if __name__ == '__main__':
    # pos = ctler.findcolor("FFFF8B", template=r"E:\Kin-Desktop\3333.png")
    # print(pos)
    res = ctler.ocr(template=r"E:\Kin-Picture\555.png", mode=1)
    print(res)
