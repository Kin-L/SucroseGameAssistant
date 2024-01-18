import sys
from tools.environment import *


class Task:
    def __init__(self):
        self.task_all = None
        self.task = None

    @staticmethod
    def indicate(msg: str, mode=2, his=True, log=True):
        logger(msg)
