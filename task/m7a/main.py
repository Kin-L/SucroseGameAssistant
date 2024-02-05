# -*- coding:gbk -*-
from ..default_task import Task
from tools.environment import *
from tools.software import get_pid, close
import traceback
import os
import yaml


class TaskM7A(Task):
    def __init__(self):
        super().__init__()

    def m7a_start(self, task: type[dir]):
        _k = False
        self.task = task
        self.indicate("开始任务:三月七助手")
        # noinspection PyBroadException
        try:
            # MAA关闭并初始化
            pid = get_pid("March7th Assistant.exe")
            if pid is not None:
                self.indicate("三月七助手已启动,准备重启")
                close(pid)
            _path = self.task["启动"]["m7a_path"]
            if os.path.isfile(_path):
                dire, name = os.path.split(_path)
                if name == "March7th Assistant.exe":
                    pass
                elif name == "March7th Launcher.exe":
                    _path = dire + "/March7th Launcher.exe"
                else:
                    self.indicate("三月七助手,无效启动路径")
                    raise ValueError("三月七助手,无效启动路径")
            else:
                self.indicate("三月七助手,无效启动路径")
                raise ValueError("三月七助手,无效启动路径")
            env.set_soft(None, [True, "ConsoleWindowClass", "m7a"])
            env.soft.set_path(_path)
            # 修改M7A运行设置
            config_yaml = os.path.split(_path)[0] + "/config.yaml"
            with open(config_yaml, 'r', encoding='utf-8') as f:
                _dir = yaml.load(stream=f, Loader=yaml.FullLoader)
            current = _dir["after_finish"]
            _dir["after_finish"] = "Exit"
            with open(config_yaml, 'w', encoding='utf-8', ) as f:
                yaml.dump(_dir, f, encoding='utf-8', allow_unicode=True)
            # 运行-结束
            _run = env.soft.run(fls=False, tit="m7a")
            if _run:
                self.indicate("三月七助手运行中...")
                _dire = os.path.split(_path)[0] + "/logs/"
                _name = os.listdir(_dire)[-1]
                _path = _dire + _name
                while 1:
                    wait(10000)
                    f = open(_path, encoding='utf-8')
                    if "游戏退出成功" in f.readlines()[-2]:
                        break
                # env.soft.kill()
                self.indicate("三月七助手运行完成")
            else:
                self.indicate("三月七助手启动失败")
                _k = True
            # 修改回M7A运行设置
            with open(config_yaml, 'r', encoding='utf-8') as f:
                _dir = yaml.load(stream=f, Loader=yaml.FullLoader)
            _dir["after_finish"] = current
            with open(config_yaml, 'w', encoding='utf-8', ) as f:
                yaml.dump(_dir, f, encoding='utf-8', allow_unicode=True)
        except Exception:
            self.indicate("任务执行异常:三月七助手", log=False)
            logger.error("任务执行异常:三月七助手\n%s" % traceback.format_exc())
            _k = True
        self.indicate("完成任务:三月七助手")
        return _k


if __name__ == '__main__':
    pass
