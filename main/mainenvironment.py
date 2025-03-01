from main.tools.environment import Environment, logger


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
        self.ocrdir = ""

        self.version = str  # 版本号
        self.last_runtime = str  # 上一次任务执行时间
        self.current_mute = bool  # 静音状态
        self.now_config = dict  # 执行任务的配置
        self.setting = 1  # 主界面面板状态
        self.download = None
        self.config_name, self.config_type = [], []  # 配置状态
        self.name, self.load = [], []  # 模块状态
        # 循环线程 任务线程 更新线程
        self.thread = None
        self.hotkeystop = None

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
