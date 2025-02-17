from ..default_task import Task
from tools.environment import *
from tools.software import get_pid, close, find_hwnd
from ruamel.yaml import YAML

class Taskzzz(Task):
    def __init__(self):
        super().__init__()

    def zzz_start(self, task: type[dir]):
        _k = False
        self.task = task
        self.indicate("开始任务:绝区零助手")
        # noinspection PyBroadException
        try:
            #判断路径
            _path = self.task["启动"]["zzz_path"]
            if isfile(_path):
                dire, name = split(_path)
                if name == "OneDragon Scheduler.exe":
                    pass
                elif name == "OneDragon Launcher.exe":
                    _path = dire + "/OneDragon Scheduler.exe"
                else:
                    self.indicate("绝区零一条龙,无效启动路径")
                    raise ValueError("绝区零一条龙,无效启动路径")
            else:
                self.indicate("绝区零助手,无效启动路径")
                raise ValueError("绝区零助手,无效启动路径")
            env.set_soft(None, [True, "ConsoleWindowClass", "OneDragon"])
            env.soft.set_path(_path)
            # 一条龙关闭并初始化
            pid = get_pid("OneDragon Launcher.exe")
            if pid is not None:
                self.indicate("绝区零一条龙已启动,准备重启")
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
                self.indicate("绝区零一条龙运行中...")
                wait(100000)
                while 1:
                    wait(10000)
                    if not find_hwnd((1, "UnityWndClass", "绝区零")):
                        break
                # env.soft.kill()
                self.indicate("绝区零一条龙运行完成")
            else:
                self.indicate("绝区零一条龙启动失败")
                return True
        except Exception:
            self.indicate("任务执行异常:绝区零助手", log=False)
            logger.error("任务执行异常:绝区零助手\n%s" % format_exc())
            _k = True
        self.indicate("完成任务:绝区零助手")
        return _k
    
if __name__ == '__main__':
    pass
