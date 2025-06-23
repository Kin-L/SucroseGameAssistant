from maincode.tools.main import GetTracebackInfo, logger
from maincode.tools.myclass import SGAStop
from maincode.main.maingroup import sg
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal, QObject
from typing import Optional, Callable
from .update import update
from maincode.main.info import info


class SGAMainThread(QObject):
    # update: Callable
    start: Optional[Callable] = None
    """
    info: 发送信息到指示栏（str)；
          默认在信息前添加时间前缀（默认值True），可使用False取消时间前缀 "%H:%M:%S "
    infoHead: 添加日期行  "%Y-%m-%d"
    infoEnd: 添加结束行 "-" * n
    """
    infoAdd: pyqtBoundSignal = pyqtSignal(str, bool)
    infoHead: pyqtBoundSignal = pyqtSignal()
    infoEnd: pyqtBoundSignal = pyqtSignal()
    finish: pyqtBoundSignal = pyqtSignal()

    def __init__(self, tasktype: str, para: dict):
        super().__init__()
        self.tasktype = tasktype
        self.para = para
        self.ctler = None

    def run(self):
        if self.tasktype == "update":
            self.__class__.start = update
            self.start()
        elif self.tasktype in ["current", "timed"]:
            num = sg.modules.FindItem(self.para["ModuleKey"])[-1]
            _func = sg.modules.Tasks[num]
            self.__class__.start = _func
            from maincode.tools.controller.main import ctler
            self.ctler = ctler
            try:
                self.start()
                info.TaskError = False
            except SGAStop:
                pass
            except RuntimeError as e:
                info.TaskError = True
                _str = GetTracebackInfo(e)
                self.send(f"任务执行异常")
                logger.error(_str+f"任务执行异常")
            self.ctler.OCR.disable()
        self.finish.emit()

    def send(self, msg: [str, int], addtime: bool = True):
        if isinstance(msg, str):
            self.infoAdd.emit(msg, addtime)
        else:
            self.infoEnd.emit() if msg else self.infoHead.emit()
