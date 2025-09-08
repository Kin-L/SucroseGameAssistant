import time
from PyQt5.QtCore import QObject, pyqtBoundSignal, pyqtSignal
from maincode.tools.controller.operate import Operate
from maincode.tools.core.logger import logger
from maincode.tools.system.other import CmdRun
from maincode.tools.system.window import GetWindow
from win32gui import FindWindow


class Controller(QObject, Operate):
    infoAdd: pyqtBoundSignal = pyqtSignal(str, bool)
    infoHead: pyqtBoundSignal = pyqtSignal()
    infoEnd: pyqtBoundSignal = pyqtSignal()

    def __init__(self):
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
        self.window = GetWindow(para)
        self.ChangeReference(ref)
        self.ChangeOperate(self.window.rect)
        logger.info(f"当前窗口：{self.window.rect}")

    def RunProg(self, _cmdline, _clsandtit, _wait=(0.2, 10), _retry: int = 10):
        _interval, _fre = _wait
        for _ in range(_retry):
            for _ in range(_fre):
                _list = [FindWindow(*item) for item in _clsandtit]
                for i in _list:
                    if i:
                        return i
                else:
                    self.wait(_interval)
            else:
                CmdRun(_cmdline)
        for _ in range(_fre):
            _list = [FindWindow(*item) for item in _clsandtit]
            for i in _list:
                if i:
                    return i
            else:
                self.wait(_interval)
        else:
            return 0

    def send(self, msg: [str, int], addtime: bool = True):
        if isinstance(msg, str):
            self.infoAdd.emit(msg, addtime)
        else:
            self.infoEnd.emit() if msg else self.infoHead.emit()


ctler = Controller()
