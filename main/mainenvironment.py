from main.tools.environment import Environment, logger
from main.thread.main import SGAThread
import keyboard


class SGAEnvironment(Environment):
    def __init__(self):
        super().__init__()
        # 主配置
        self.current_work_path = str
        self.timer = dict
        self.update = bool
        self.lock = bool
        self.config = str
        self.current = dict
        self.launch = dict

        self.version = str  # 版本号
        self.last_runtime = str  # 上一次任务执行时间
        self.current_mute = bool  # 静音状态
        self.now_config = dict  # 执行任务的配置
        self.setting = 1  # 主界面面板状态
        self.config_name, self.config_type = [], []  # 配置状态
        self.name, self.load = [], []  # 模块状态
        # 循环线程 任务线程 更新线程
        self.thread = None
        self.hotkeystop = None
        self.hotkeystop.enable = self.hotkeystop_enable
        self.hotkeystop.disable = self.hotkeystop_disable

    def thread_load(self):
        if self.update:
            self.thread = SGAThread("autoupdate")
        else:
            self.thread = SGAThread("cycle")
        self.thread.start()

    def hotkeystop_enable(self):
        keyboard.add_hotkey("ctrl+/", self.thread_stop)

    @staticmethod
    def hotkeystop_disable():
        # noinspection PyBroadException
        try:
            keyboard.remove_hotkey("ctrl+/")
        except Exception:
            logger.debug("快捷键功能未建立：ctrl+/")

    def thread_stop(self):
        keyboard.remove_hotkey("ctrl+/")
        if self.thread.isRunning():
            self.thread.terminate()
            from time import sleep
            from datetime import datetime
            _now = datetime.now()
            if sme.last_runtime == _now.strftime("%Y-%m-%d %H:%M"):
                from main.ui.mainwindow.connect import save_env_data
                _num = (60 - int(_now.strftime("%S"))) // 15 + 1
                for i in range(_num):
                    sleep(15)
                    save_env_data()
            self.thread = SGAThread("cycle")
            self.thread.start()
        else:
            logger.debug("线程早已关闭")

    def logger_environment_info(self):
        _str = (f"\n运行环境:\n"
                f"  工作目录:{self.workdir}\n"
                f"  CPUFeature:{self.cpu_feature}\n"
                f"  系统:{self.platform}\n"
                f"显示器:")
        for i, (w, h), (x, y) in self.monitors:
            _str += f"\n  编号:{i} 分辨率:{w}×{h} 位置:{x},{y}"
        logger.info(_str)


sme = SGAEnvironment()

if __name__ == '__main__':
    pass
