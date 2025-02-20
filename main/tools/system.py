from subprocess import run as cmd_run
from psutil import process_iter


# 从exe名称获取pid
def get_pid(name):
    for proc in process_iter():
        # noinspection PyBroadException
        try:
            if proc.name() == name:
                return proc.pid
        except Exception:
            continue
    return 0


# 关闭进程
def close(_v):
    if isinstance(_v, int):
        # 根据pid杀死进程
        process = 'taskill /f /pid %s' % _v
        cmd_run(process)
    elif isinstance(_v, str):
        # 根据进程名杀死进程
        pro = 'taskill /f /im %s' % _v
        cmd_run(pro)
    else:
        raise ValueError(f"close异常传输值：{_v}")
