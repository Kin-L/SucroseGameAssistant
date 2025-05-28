import os
import subprocess
from datetime import datetime
from ..default_task import Task
from traceback import format_exc
from tools.environment import wait, SGAStop
from tools.software import get_pid, close

class TaskKaa(Task):
    def __init__(self):
        super().__init__()

    def kaa_start(self, task: type[dir]):
        self.task = task
        self.indicate("开始任务:琴音小助手")
        # noinspection PyBroadException
        try:
            #判断路径
            base_path = self.task["启动"]["kaa_path"]
            if not os.path.exists(base_path):
                self.indicate("琴音小助手,程序文件夹不存在")
                raise ValueError("琴音小助手,路径错误")
            kaa_path = os.path.join(base_path, "WPy64-310111", "python-3.10.11.amd64", "Scripts", "kaa.exe")
            config_path = os.path.join(base_path, "config.json")
            log_path = os.path.join(base_path, "logs", datetime.now().strftime('logs/sga-%y-%m-%d-%H-%M-%S.log'))
            if not os.path.exists(kaa_path):
                self.indicate("琴音小助手,路径正确但未安装.需至少执行一次琴音小助手本体才能使用.")
                raise ValueError("琴音小助手,路径错误")
            if not os.path.exists(config_path):
                self.indicate("琴音小助手,配置文件不存在.需至少执行一次琴音小助手本体才能使用.")
                raise ValueError("琴音小助手,路径错误")
            self.kaa_wait(kaa_path, config_path, log_path)
            return False
        except Exception:
            self.indicate("任务执行异常:琴音小助手", log=False)
            self.indicate("任务执行异常:琴音小助手\n%s" % format_exc(), log=True)
        except SGAStop:
            raise SGAStop
        return True

    def kaa_wait(self, kaa_path, config_path, log_path):
        pid = get_pid("kaa.exe")
        if pid:
            self.indicate("琴音小助手已启动,准备重启")
            close(pid)

        self.indicate("正在启动琴音小助手...")
        self.indicate("配置文件路径：" + config_path)
        try:
            p = subprocess.Popen(
                [
                    kaa_path,
                    '--config', config_path,
                    '--log-path', log_path,
                    '--log-level', 'DEBUG',
                    '--kill-dmm',
                    '--kill-game',
                    'task', 'invoke', '*'
                ],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.indicate("琴音小助手运行中...")
            wait(10000)

            # while True:
            #     wait(10000)
            #     pid = get_pid("kaa.exe")
            #     if not pid:
            #         break
            p.wait()
            self.indicate("琴音小助手运行完成")
            return True
        except Exception as e:
            self.indicate("琴音小助手启动失败: %s" % str(e))
            return False
