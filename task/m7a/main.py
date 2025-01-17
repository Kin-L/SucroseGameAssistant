from ..default_task import Task
from tools.environment import *
from tools.software import get_pid, close, find_hwnd
from ruamel.yaml import YAML

class TaskM7A(Task):
    def __init__(self):
        super().__init__()

    def m7a_start(self, task: type[dir]):
        _k = False
        self.task = task
        self.indicate("开始任务:崩坏：星穹铁道助手")
        # noinspection PyBroadException
        try:
            #判断路径
            _path = self.task["启动"]["m7a_path"]
            if isfile(_path):
                dire, name = split(_path)
                if "March7th" in name:
                    if name == "March7th Assistant.exe":
                        pass
                    elif name == "March7th Launcher.exe":
                        _path = dire + "/March7th Launcher.exe"
                    self.m7a(_path)
                elif "OneDragon" in name:
                    if name == "OneDragon Scheduler.exe":
                        pass
                    elif name == "OneDragon Launcher.exe":
                        _path = dire + "/OneDragon Scheduler.exe"
                    self.od(_path)
                else:
                    self.indicate("崩坏：星穹铁道助手,无效启动路径")
                    raise ValueError("崩坏：星穹铁道助手,无效启动路径")
            else:
                self.indicate("崩坏：星穹铁道助手,无效启动路径")
                raise ValueError("崩坏：星穹铁道助手,无效启动路径")
        except Exception:
            self.indicate("任务执行异常:崩坏：星穹铁道助手", log=False)
            logger.error("任务执行异常:崩坏：星穹铁道助手\n%s" % format_exc())
            _k = True
        self.indicate("完成任务:崩坏：星穹铁道助手")
        return _k
    
    def m7a(self, _path):
        env.set_soft(None, [True, "ConsoleWindowClass", "m7a"])
        env.soft.set_path(_path)
        #三月七关闭并初始化
        pid = get_pid("March7th Assistant.exe")
        if pid is not None:
            self.indicate("三月七助手已启动,准备重启")
            close(pid)
        # 修改三月七运行设置
        config_yaml = os.path.join(split(_path)[0],"config.yaml")
        yaml = YAML()
        yaml.preserve_quotes = True
        with open(config_yaml, 'r', encoding='utf-8') as f:
            _dir = yaml.load(f)
        if _dir["after_finish"] != "Exit":
            _dir["after_finish"] = "Exit"
            with open(config_yaml, 'w', encoding='utf-8', ) as f:
                yaml.dump(_dir, f)
        # 运行-结束
        _run = env.soft.run(fls=False, tit="m7a")
        if _run:
            self.indicate("三月七助手运行中...")
            while 1:
                wait(10000)
                if not find_hwnd((1, "UnityWndClass", "崩坏：星穹铁道")):
                    break
            # env.soft.kill()
            self.indicate("三月七助手运行完成")
        else:
            self.indicate("三月七助手启动失败")
            return True
        # M7A关闭
        pid = get_pid("PaddleOCR-json.exe")
        if pid is not None:
            self.indicate("关闭三月七助手")
            close(pid)
    
    def od(self, _path):
        env.set_soft(None, [True, "ConsoleWindowClass", "od"])
        env.soft.set_path(_path)
        # 一条龙关闭并初始化
        pid = get_pid("OneDragon Launcher.exe")
        if pid is not None:
            self.indicate("星铁一条龙已启动,准备重启")
            close(pid)
        # 修改一条龙运行设置
        config_yaml = os.path.join(split(_path)[0],"config","zzz_one_dragon.yml")
        yaml = YAML()
        yaml.preserve_quotes = True
        with open(config_yaml, 'r', encoding='utf-8') as f:
            _dir = yaml.load(f)
        if _dir["after_done"] != "关闭游戏":
            _dir["after_done"] = "关闭游戏"
            with open(config_yaml, 'w', encoding='utf-8', ) as f:
                yaml.dump(_dir, f)
        # 运行-结束
        _run = env.soft.run(fls=False, tit="OneDragon")
        if _run:
            self.indicate("星铁一条龙运行中...")
            while 1:
                wait(10000)
                if not find_hwnd((1, "UnityWndClass", "崩坏：星穹铁道")):
                    break
            # env.soft.kill()
            self.indicate("星铁一条龙运行完成")
        else:
            self.indicate("星铁一条龙启动失败")
            return True

if __name__ == '__main__':
    pass
