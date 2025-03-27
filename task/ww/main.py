from ..default_task import Task
from tools.environment import *
from tools.software import find_hwnd
from win32gui import FindWindow
from subprocess import run as cmd_run

class Taskww(Task):
    def __init__(self):
        super().__init__()

    def ww_start(self, task: type[dir]):
        _k = False
        self.task = task
        self.indicate("开始任务:鸣潮助手")
        # noinspection PyBroadException
        try:
            #判断路径
            _path = os.path.expandvars("%APPDATA%\Microsoft\Windows\Start Menu\Programs\ok-ww Daily Task exit_after.lnk")
            if not isfile(_path):
                self.indicate(_path)
                self.indicate("未找到ok-ww启动路径")
                raise ValueError("未找到ok-ww启动路径")
            # 打开一条龙
            cmd = f"start \"\" \"{_path}\""
            for n in range(2):
                cmd_run(cmd, shell=True)
                for sec in range(10):
                    wait(1000)
                    hwnd = FindWindow(None, "OK-WW")
                    if hwnd:
                        self.indicate("一条龙启动成功")
                        wait(500)
                        break
                    elif sec == 9:
                        self.indicate("ok-ww启动异常")
                        return True
            # 检测关闭
            wait(30000)
            while 1:
                wait(10000)
                if not find_hwnd((1, "UnityWndClass", "Wuthering Waves")):
                    break
        except Exception:
            self.indicate("任务执行异常:鸣潮助手", log=False)
            logger.error("任务执行异常:鸣潮助手\n%s" % format_exc())
            _k = True
        self.indicate("完成任务:鸣潮助手")
        return _k
    
if __name__ == '__main__':
    pass
