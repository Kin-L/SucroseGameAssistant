from json import load, dump
from ..default_task import Task
from tools.environment import *
from tools.software import get_pid, close, find_hwnd
from os.path import isfile, split, join, exists
from os import remove
from traceback import format_exc


class TaskCommon(Task):
    def __init__(self):
        super().__init__()

    def common_start(self, task: type[dir]):
        _k = False
        self.task = task
        self.indicate("开始任务:通用执行")
        # noinspection PyBroadException
        try:
            pass
        except Exception:
            self.indicate("任务执行异常:通用执行", log=False)
            logger.error("任务执行异常:通用执行\n%s" % format_exc())
            _k = True
        self.indicate("完成任务:通用执行")
        return _k


if __name__ == '__main__':
    pass
