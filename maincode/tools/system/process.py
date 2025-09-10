from typing import Union
import psutil
from maincode.tools.core.logger import logger


# 从exe名称获取pid
def GetPid(name: str) -> int:
    for proc in psutil.process_iter():
        try:
            if proc.name() == name:
                return proc.pid
        except Exception as e:
            logger.warning(f"获取进程PID时异常: {e}")
            continue
    return 0


# 关闭进程
def killprocess(_process: Union[int, str]):
    if isinstance(_process, int):
        _pid = _process
    elif isinstance(_process, str):
        _pid = GetPid(_process)
    else:
        raise ValueError(f"close异常传输值：{_process}")
    try:
        process = psutil.Process(_pid)
        process.terminate()
        gone, still_alive = psutil.wait_procs([process], timeout=5)
        if still_alive:
            process.kill()
            logger.warning(f"强制杀死进程 PID: {_pid}")
        else:
            logger.info(f"成功终止进程 PID: {_pid}")
        return 0
    except psutil.NoSuchProcess:
        logger.error(f"进程不存在 PID: {_pid}")
        return 1
    except psutil.AccessDenied:
        logger.error(f"无权限终止进程 PID: {_pid}")
        return 2
