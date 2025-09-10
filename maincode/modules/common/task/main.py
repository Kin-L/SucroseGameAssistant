import subprocess
import win32gui
import psutil
from maincode.config.configctrl import scc
from maincode.tools.core.baseclass import SGAStop
from maincode.tools.core.logger import logger
from maincode.tools.system.notification import GetTracebackInfo
import os

from maincode.tools.system.other import CmdRun
from maincode.tools.system.window import find_window_by_title
from maincode.tools.system.window import GetWindow


def taskstart(self):
    """通用任务执行入口"""
    try:

        # 启动主程序
        start_mode = self.para.get("StartMode", 0)
        cmdline = self.para.get("CMDLine", "")
        if not cmdline:
            raise ValueError("未设置启动路径")
        if start_mode == 0:
            cmd_line = f"start \"\" \"{cmdline}\""
        elif start_mode == 1:
            cmd_line = cmdline
        else:
            raise ValueError("未知启动模式")
        window_name = self.para.get("StartProcess", None)
        if window_name:
            for _ in range(10):
                win = None
                for _ in range(10):
                    win = GetWindow(window_name)
                    if win:
                        break

                    else:
                        self.ctler.wait(0.4)
                else:
                    CmdRun(cmd_line)
                if win:
                    break
            else:
                raise TimeoutError("启动程序超时")
            self.start_hwnd = win.GetHwnd()
            self.send(f"检测到窗口：{window_name} 句柄:{self.start_hwnd}")

        wait_time = self.para.get("WaitTimeBefore")
        if wait_time:
            self.send(f"开始前等待 {wait_time} 秒")
            self.ctler.wait(wait_time)

        if self.para.get("StartOperateMode"):
            _execute_start_operation(self)

        # 后置等待
        self._handle_post_wait()

        # 结束条件判断
        self._monitor_finish_condition()

    except SGAStop:
        raise  # 传递停止信号
    except Exception as e:
        _str = GetTracebackInfo(e)
        logger.error(_str + "任务执行异常:通用执行")
        scc.info.TaskError = True
    finally:
        self._cleanup_processes()
        self.send("完成任务:通用执行")


def _execute_start_operation(self):

    self.ctler.ChooseWindow(self.start_hwnd, (1920, 1080))
    """执行启动操作"""
    op_type = self.para.get("启动操作类型", 0)

    if op_type == 0:
        self.send("无启动操作")
        return

    # 获取目标进程ID
    target_pid = self.para.get("启动判断进程名")
    if target_pid:
        target_pid = find_pid_from_name(target_pid)
        self.aproc = psutil.Process(target_pid) if target_pid else None
    else:
        target_pid = self.pid

    if not target_pid:
        raise RuntimeError("未找到目标进程")

    # 获取窗口区域
    hwnd = find_hwnd_from_pid(target_pid)
    if not hwnd:
        raise RuntimeError("未找到目标窗口")

    fram = win32gui.GetWindowRect(hwnd)
    zone = self._get_operation_zone(fram, "启动判断指定区域")

    # 执行对应操作
    op_content = self.para.get("启动操作内容", "")
    if op_type == 1:  # 文本点击
        self.send(f"等待文本: {op_content}")
        pos = self.ctler.wait_text(op_content, zone)
        self.ctler.click(pos)
    elif op_type == 2:  # 图像点击
        self.send(f"等待图像: {op_content}")
        pos = self.ctler.wait_pic(op_content, zone)
        self.ctler.click(pos)
    elif op_type == 3:  # 快捷键
        self.send(f"执行快捷键: {op_content}")
        self.ctler.add_press(op_content)


def _handle_post_wait(self):
    """处理开始后等待"""
    wait_time = self.para.get("开始后等待时间")
    if wait_time:
        self.send(f"开始后等待 {wait_time} 秒")
        self.ctler.wait(wait_time)


def _monitor_finish_condition(self):
    """监控结束条件"""
    # 获取目标进程
    target_pid = self.para.get("结束判断进程名")
    if target_pid:
        target_pid = find_pid_from_name(target_pid)
        self.eproc = psutil.Process(target_pid) if target_pid else None
    else:
        target_pid = self.pid

    if not target_pid or not psutil.pid_exists(target_pid):
        raise RuntimeError("结束判断目标进程不存在")

    proc = psutil.Process(target_pid)
    end_type = self.para.get("结束判断类型", 0)
    loop_config = self.para.get("判断循环", (3, 5))  # 默认3次，间隔5秒
    num, sec = loop_config if isinstance(loop_config, (list, tuple)) else (3, 5)

    self.send(f"开始监控结束条件 (类型: {end_type})")

    if end_type == 0:  # 进程退出
        while proc.is_running():
            self.ctler.wait(5)

    elif end_type == 3:  # CPU利用率
        n = 0
        threshold = float(self.para.get("结束判断内容", 5.0))
        while True:
            if proc.cpu_percent(0.1) > threshold:
                self.ctler.wait(5)
            else:
                n += 1
                if n >= num:
                    break
                self.ctler.wait(sec)

    else:  # 文本/图像识别
        hwnd = find_hwnd_from_pid(target_pid)
        fram = win32gui.GetWindowRect(hwnd) if hwnd else (0, 0, 0, 0)
        zone = self._get_operation_zone(fram, "结束判断指定区域")
        content = self.para.get("结束判断内容", "")
        n = 0

        while True:
            found = False
            if end_type == 1:  # 文本匹配
                found = self.ctler.find_text(content, zone)
            elif end_type == 2:  # 图像匹配
                found = self.ctler.find_pic(content, zone)[0]

            if found:
                n += 1
                if n >= num:
                    break
                self.ctler.wait(sec)
            else:
                self.ctler.wait(5)


def _get_operation_zone(self, fram, config_key):
    """计算操作区域"""
    zone_config = self.para.get(config_key)
    if zone_config:
        x1, y1, x2, y2 = zone_config
        return (
            fram[0] + x1,
            fram[1] + y1,
            fram[0] + x2,
            fram[1] + y2
        )
    return "ALL"  # 全区域


def _cleanup_processes(self):
    """清理进程资源"""
    if self.para.get("关闭软件", False):
        for p in [self.proc, self.aproc, self.eproc]:
            if p and p.is_running():
                try:
                    p.kill()
                    self.send(f"已关闭进程: {p.name()}")
                except psutil.NoSuchProcess:
                    pass
                except Exception as e:
                    self.send(f"关闭进程失败: {str(e)}")
