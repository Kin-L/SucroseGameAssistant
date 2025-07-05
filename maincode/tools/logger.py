from logging import getLogger, FileHandler, Formatter, StreamHandler
from os import path, makedirs, remove
from time import strftime, localtime
from colorlog import ColoredFormatter
import glob


class Logger:
    def __init__(self):
        self.logger = getLogger('SGA')
        self.logger.date = strftime("%Y-%m-%d", localtime())
        self.logger.propagate = False
        self.logger.setLevel("DEBUG")
        if not path.exists("personal/logs"):
            makedirs("personal/logs")
        self.file_handler = FileHandler(rf"personal\logs\{self.logger.date}.log", encoding="utf-8")  # midnight
        file_formatter = Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt="%H:%M:%S")
        self.file_handler.setFormatter(file_formatter)
        self.logger.addHandler(self.file_handler)

        self.console_handler = StreamHandler()
        # 定义颜色输出格式
        color_formatter = ColoredFormatter(
            '%(log_color)s%(asctime)s | %(levelname)s | %(message)s',
            log_colors={
                'DEBUG': 'green',
                'INFO': 'cyan',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            datefmt="%H:%M:%S"
        )
        self.console_handler.setFormatter(color_formatter)
        self.logger.addHandler(self.console_handler)
        self.logger.new_handler = self.new_handler

    def getlogger(self):
        return self.logger

    def new_handler(self, date):
        self.logger.date = date
        self.logger.removeHandler(self.file_handler)
        self.file_handler = FileHandler(f"personal/logs/{date}.log", encoding="utf-8")  # midnight
        file_formatter = Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt="%H:%M:%S")
        self.file_handler.setFormatter(file_formatter)
        self.logger.addHandler(self.file_handler)

        # 保留30天日志
        files = glob.glob(path.join("personal/logs", '*'))
        files = [f for f in files if path.isfile(f)]
        if len(files) <= 30:
            return
        files.sort(key=lambda x: path.getmtime(x), reverse=True)
        files_to_delete = files[30:]
        for file_to_delete in files_to_delete:
            try:
                remove(file_to_delete)
            except Exception as e:
                print(f"{e}")

        # 保留40张错误截图
        files = glob.glob(path.join("personal/errorsc", '*'))
        files = [f for f in files if path.isfile(f)]
        if len(files) <= 30:
            return
        files.sort(key=lambda x: path.getmtime(x), reverse=True)
        files_to_delete = files[30:]
        for file_to_delete in files_to_delete:
            try:
                remove(file_to_delete)
            except Exception as e:
                print(f"{e}")


if __name__ == '__main__':
    pass
