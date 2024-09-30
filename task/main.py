from task.maa.main import TaskMAA
from task.genshin.main import TaskGenshin
from task.kleins.main import TaskKleins
from task.m7a.main import TaskM7A
from task.snow.main import TaskSnow


class TaskRun(TaskKleins, TaskGenshin, TaskMAA, TaskM7A, TaskSnow):
    def task_start(self, task):
        _k = False
        print(task)
        # 运行
        if task["模块"] == 0:
            for i in range(5):
                single_task = task["配置%s" % i]
                if single_task["name"] == "<未选择>":
                    self.indicate(f"计划{i+1}未选择。")
                else:
                    single_task["关闭软件"] = True
                    if self.single_run(single_task):
                        _k = True
        else:
            if self.single_run(task):
                _k = True
        return _k

    def single_run(self, task):
        _k = False
        if task["模块"] == 1:
            TaskKleins.__init__(self)
            if self.kleins_start(task):
                _k = True
        elif task["模块"] == 2:
            TaskGenshin.__init__(self)
            if self.genshin_start(task):
                _k = True
        elif task["模块"] == 3:
            TaskMAA.__init__(self)
            if self.maa_start(task):
                _k = True
        elif task["模块"] == 4:
            TaskM7A.__init__(self)
            if self.m7a_start(task):
                _k = True
        elif task["模块"] == 5:
            TaskSnow.__init__(self)
            if self.snow_start(task):
                _k = True
        else:
            self.indicate("error:未知模块。")
            _k = True
        return _k


if __name__ == '__main__':
    pass
