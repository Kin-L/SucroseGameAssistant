from PyQt5.QtCore import QThread, pyqtSignal
from tools.environment import *
# from genshin.main import TaskGenshin
from task.maa.main import TaskMAA
from task.genshin.main import TaskGenshin


class TaskRun(QThread):
    indicate = pyqtSignal(str)
    accomplish = pyqtSignal(int)

    def __init__(self, task_dir):  # mode true：集成运行 false：独立运行
        super(TaskRun, self).__init__()
        self.task_dir = task_dir
        self.task_run = type[classmethod]
        self.after_task = type[classmethod]
        self.wait_task = WaitStop(self.after_task)
        self.wait_task.send.connect(self.send_text)

    def run(self):
        self.task_dir["current_mute"] = get_mute()
        if self.task_dir["运行"][0] and not self.task_dir["current_mute"]:
            change_mute()
        if self.task_dir["mode"]:
            self.send_text("开始执行定时计划：\n  " + self.task_dir["name"])
            notify("开始定时任务", "任务名：" + self.task_dir["name"])
        else:
            self.send_text("开始执行实时计划。")
        # 运行
        if self.task_dir["模块"] == 0:
            for i in range(5):
                task_dir = self.task_dir["模块"]["配置%s" % i]
                if task_dir:
                    task_dir["mode"] = False
                    self.single_run(task_dir)
                else:
                    print("计划为空，连续执行结束。")
        else:
            self.task_dir["mode"] = True
            self.single_run(self.task_dir)
        # 结束
        if self.task_dir["运行"][2] == 1:
            msg = "\n任务完成，10s后熄屏。\n可按组合键“ctrl+/”取消。"
            self.after_task = WaitTask(10, "screen_off")
            # self.wait_task = WaitStop(self.after_task)
            self.after_task.start()
            self.wait_task.start()
            self.after_task.accomplish.connect(lambda: self.wait_task.terminate())
        elif self.task_dir["运行"][2] == 2:
            msg = "\n任务完成，60s后睡眠。\n可按组合键“ctrl+/”取消。"
            self.after_task = WaitTask(60, "sleep")
            # self.wait_task = WaitStop(self.after_task)
            self.after_task.start()
            self.wait_task.start()
            self.after_task.accomplish.connect(lambda: self.wait_task.terminate())
        else:
            msg = " "
        if self.task_dir["name"]:
            notify("定时计划执行结束", "任务名：%s%s" % (self.task_dir["name"], msg))
            self.send_text("定时计划执行结束：\n%s%s" % (self.task_dir["name"], msg))
        else:
            notify("实时计划执行结束", msg)
            self.send_text("实时计划执行结束。%s" % msg)
        now_mute = get_mute()
        if (now_mute != self.task_dir["current_mute"]) and (now_mute == self.task_dir["运行"][0]):
            wait(1200)
            change_mute()
        self.kill(1)

    def send_text(self, msg: str):
        self.indicate.emit(msg)
        # logging(msg)

    def single_run(self, task_dir):
        if task_dir["模块"] == 1:
            self.task_run = TaskMAA(self.task_dir)
        elif task_dir["模块"] == 2:
            self.task_run = TaskGenshin(self.task_dir)
        self.task_run.indicate.connect(self.send_text)
        self.task_run.accomplish.connect(self.kill)
        self.task_run.start()

    def kill(self, mode):
        self.accomplish.emit(mode)
        self.terminate()


class WaitStop(QThread):
    send = pyqtSignal(str)

    def __init__(self, task):  # mode true：集成运行 false：独立运行
        super(WaitStop, self).__init__()
        self.task = task

    def run(self):
        import keyboard
        keyboard.wait("ctrl+/")
        self.task.terminate()


class WaitTask(QThread):
    accomplish = pyqtSignal(int)

    def __init__(self, wait_time: int, mode: str, order: str = ""):  # mode true：集成运行 false：独立运行
        super(WaitTask, self).__init__()
        self.task = [wait_time, mode, order]

    def run(self):
        for i in range(self.task[0]):
            wait(1000)
        self.accomplish.emit(0)
        if self.task[1] == "kill":
            close(get_pid(self.task[2]))
        elif self.task[1] == "screen_off":
            screen_off()
        elif self.task[1] == "sleep":
            cmd_run("powercfg - h off")
            cmd_run("rundll32.exe powrprof.dll, SetSuspendState 0, 1, 0")


if __name__ == '__main__':
    pass
