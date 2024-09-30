from logging import getLogger, FileHandler, Formatter, StreamHandler
from os.path import exists
from os import makedirs
from datetime import datetime
from colorama import init
from .titleformatter import TitleFormatter


class Logger:
    def __init__(self):
        date = datetime.now().strftime("%Y-%m-%d")
        self.logger = getLogger('SGA')
        self.logger.propagate = False
        self.logger.setLevel("DEBUG")
        if not exists("personal/logs"):
            makedirs("personal/logs")
        file_handler = FileHandler(rf"personal\logs\{date}.log", encoding="utf-8")
        file_formatter = Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt="%H:%M:%S")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel("DEBUG")
        self.logger.addHandler(file_handler)

        self.console_handler = StreamHandler()
        console_formatter = ColoredFormatter('%(asctime)s | %(levelname)s | %(message)s', datefmt="%H:%M:%S")
        self.console_handler.setFormatter(console_formatter)
        self.console_handler.setLevel("INFO")

        self.logger.enable_console = self.enable_console
        self.logger.disable_console = self.disable_console

    def get_logger(self):
        return self.logger

    def enable_console(self):
        self.logger.addHandler(self.console_handler)
        self.logger.hr = TitleFormatter.format_title

    def disable_console(self):
        self.logger.removeHandler(self.console_handler)


class ColoredFormatter(Formatter):
    init(autoreset=True)
    COLORS = {
        'DEBUG': '\033[94m',  # 蓝色
        'INFO': '\033[92m',   # 绿色
        'WARNING': '\033[93m',  # 黄色
        'ERROR': '\033[91m',   # 红色
        'CRITICAL': '\033[91m',  # 红色
        'RESET': '\033[0m'   # 重置颜色
    }

    def format(self, record):
        log_level = record.levelname
        color_start = self.COLORS.get(log_level, self.COLORS['RESET'])
        color_end = self.COLORS['RESET']
        record.levelname = f"{color_start}{log_level}{color_end}"
        return super().format(record)
