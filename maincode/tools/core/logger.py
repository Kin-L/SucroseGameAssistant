from logging import getLogger, FileHandler, Formatter, StreamHandler, Logger as PyLogger
from os import path, makedirs, remove
from time import strftime, localtime
from colorlog import ColoredFormatter
import glob


class Logger:
    LOG_DIR = "personal/logs"
    ERROR_SCREENSHOT_DIR = "personal/errorsc"
    KEEP_LOG_DAYS = 30
    KEEP_SCREENSHOT_COUNT = 30

    def __init__(self):
        self.logger: PyLogger = getLogger('SGA')
        self.logger.date = strftime("%Y-%m-%d", localtime())
        self.logger.propagate = False
        self.logger.setLevel("DEBUG")

        # 确保日志目录存在
        self._ensure_directory_exists(self.LOG_DIR)

        # 初始化文件处理器
        self.file_handler = self._create_file_handler(self.logger.date)
        self.logger.addHandler(self.file_handler)

        # 初始化控制台处理器
        self.console_handler = StreamHandler()
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

    @staticmethod
    def _ensure_directory_exists(directory: str):
        """确保指定目录存在"""
        try:
            if not path.exists(directory):
                makedirs(directory)
        except Exception as e:
            print(f"Failed to create directory {directory}: {e}")
            raise

    def _create_file_handler(self, date: str) -> FileHandler:
        """创建并返回一个文件处理器"""
        log_path = path.join(self.LOG_DIR, f"{date}.log")
        handler = FileHandler(log_path, encoding="utf-8")
        formatter = Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt="%H:%M:%S")
        handler.setFormatter(formatter)
        return handler

    def getlogger(self) -> PyLogger:
        return self.logger

    def new_handler(self, date: str):
        """切换日志日期并清理旧日志"""
        self.logger.removeHandler(self.file_handler)
        self.file_handler.close()
        self.logger.date = date
        self.file_handler = self._create_file_handler(date)
        self.logger.addHandler(self.file_handler)

        # 清理旧日志文件
        self._cleanup_old_files(self.LOG_DIR, self.KEEP_LOG_DAYS)

        # 清理旧错误截图
        self._cleanup_old_files(self.ERROR_SCREENSHOT_DIR, self.KEEP_SCREENSHOT_COUNT)

    def _cleanup_old_files(self, directory: str, keep_count: int):
        """保留指定数量的最新文件，删除其余文件"""
        try:
            if not path.exists(directory):
                return
            files = [f for f in glob.glob(path.join(directory, '*')) if path.isfile(f)]
            if len(files) <= keep_count:
                return
            files.sort(key=lambda x: path.getmtime(x), reverse=True)
            files_to_delete = files[keep_count:]
            for file_to_delete in files_to_delete:
                try:
                    remove(file_to_delete)
                except Exception as e:
                    self.logger.warning(f"Failed to delete file {file_to_delete}: {e}")
        except Exception as e:
            self.logger.error(f"Error during cleanup of {directory}: {e}")


logger = Logger().getlogger()


if __name__ == '__main__':
    pass
