from logging import getLogger, FileHandler, Formatter, StreamHandler, handlers
from os.path import exists
from os import makedirs
from datetime import datetime
from colorama import init


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


class TitleFormatter:
    @staticmethod
    def custom_len(s):
        length = 0
        for char in s:
            # 判断是否是中文字符和全角符号的Unicode范围
            if (0x4E00 <= ord(char) <= 0x9FFF) or (0xFF00 <= ord(char) <= 0xFFEF):
                length += 2
            else:
                length += 1
        return length

    @staticmethod
    def format_title(title, level=0):
        try:
            separator_length = 115
            title_lines = title.split('\n')
            separator = '+' + '-' * separator_length + '+'
            title_length = TitleFormatter.custom_len(title)
            half_separator_left = (separator_length - title_length) // 2
            half_separator_right = separator_length - title_length - half_separator_left

            if level == 0:
                formatted_title_lines = []

                for line in title_lines:
                    title_length_ = TitleFormatter.custom_len(line)
                    half_separator_left_ = (separator_length - title_length_) // 2
                    half_separator_right_ = separator_length - title_length_ - half_separator_left_

                    formatted_title_line = '|' + ' ' * half_separator_left_ + line + ' ' * half_separator_right_ + '|'
                    formatted_title_lines.append(formatted_title_line)

                print(separator)
                print('\n'.join(formatted_title_lines))
                print(separator)
            elif level == 1:
                formatted_title = '=' * half_separator_left + ' ' + title + ' ' + '=' * half_separator_right
                print(f"{formatted_title}")
            elif level == 2:
                formatted_title = '-' * half_separator_left + ' ' + title + ' ' + '-' * half_separator_right
                print(f"{formatted_title}")
        except:
            pass


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
        self.file_handler.setLevel("DEBUG")
        self.logger.addHandler(self.file_handler)

        self.console_handler = StreamHandler()
        console_formatter = ColoredFormatter('%(asctime)s | %(levelname)s | %(message)s', datefmt="%H:%M:%S")
        self.console_handler.setFormatter(console_formatter)
        self.console_handler.setLevel("INFO")

        self.logger.enable_console = self.enable_console
        self.logger.disable_console = self.disable_console
        self.logger.new_handler = self.new_handler

    def new_handler(self, date):
        self.logger.date = date
        self.logger.removeHandler(self.file_handler)
        self.file_handler = FileHandler(rf"personal\logs\{date}.log", encoding="utf-8")  # midnight
        file_formatter = Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt="%H:%M:%S")
        self.file_handler.setFormatter(file_formatter)
        self.file_handler.setLevel("DEBUG")
        self.logger.addHandler(self.file_handler)

    def get_logger(self):
        return self.logger

    def enable_console(self):
        self.logger.addHandler(self.console_handler)
        self.logger.hr = TitleFormatter.format_title

    def disable_console(self):
        self.logger.removeHandler(self.console_handler)


logger = Logger().get_logger()
