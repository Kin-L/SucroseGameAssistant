from logging import getLogger, FileHandler, Formatter, StreamHandler
from os.path import exists
from os import makedirs
from datetime import datetime
from colorlog import ColoredFormatter


class Logger:
    def __init__(self):
        self.logger = getLogger('SGA')
        self.logger.date = datetime.now().strftime("%Y-%m-%d")
        self.logger.propagate = False
        self.logger.setLevel("DEBUG")
        if not exists("personal/logs"):
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

    def get_logger(self):
        return self.logger


logger = Logger().get_logger()

if __name__ == '__main__':
    pass
