import time
import maincode.tools.system.window
from maincode.tools.controller.operate import Operate
from maincode.tools.core.logger import logger
from maincode.tools.system.other import CmdRun
from maincode.tools.system.window import GetWindow
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
        maincode.tools.system.window.foreground()
        self.ChangeReference(ref)
        self.ChangeOperate(self.window.rect)
        logger.info(f"当前窗口：{self.window.rect}")

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
