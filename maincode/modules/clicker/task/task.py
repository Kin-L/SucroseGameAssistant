import time
import os
import playsound3
from .trigger import Trigger, TRIGGER_MOUSE_LIST, TRIGGER_MAP
from ..default_task import Task
from tools.environment import *
from traceback import format_exc
from tools.system.notification import WindowsNotify

# 触发键和点击键的有效列表
TRIGGER_KEY_LIST = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",
                    "F9", "F10", "F11", "F12",
                    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                    "U", "V", "W", "X", "Y", "Z",
                    "SHIFT", "CTRL", "ALT", "WINDOWS",
                    "LEFT SHIFT", "LEFT CTRL", "LEFT ALT", "LEFT WINDOWS",
                    "RIGHT SHIFT", "RIGHT CTRL", "RIGHT ALT", "RIGHT WINDOWS",
                    "ENTER", "TAB", "BACKSPACE",
                    "LEFT", "UP", "RIGHT", "DOWN", "PAGEUP", "PAGEDOWN", "END", "HOME",
                    "CAPSLOCK", "ESC", "NUMLOCK", "PAUSE", "SPACE", "INSERT", "DELETE",
                    "PRINTSCREEN"]

CLICKER_MOUSE_LIST = ["LCLICK", "RCLICK", "MCLICK"]
CLICKER_KEY_LIST = TRIGGER_KEY_LIST  # 点击键与触发键共享有效列表


class TaskTrigger(Task):
    """连点器任务控制类"""

    def __init__(self):
        super().__init__()
        self.trigger = None
        self.switch = False  # 启用/禁用开关
        self.disable_key = None  # 禁用键

    def trigger_start(self, task: dict):
        """启动触发任务"""
        self.task = task
        self.disable_key = task.get("disablekey", "").strip()

        # 验证配置有效性
        if not self._validate_config():
            return 0

        # 初始化并启动触发器
        try:
            self.indicate("开始任务:连点器")
            env.mode(2)
            self._show_task_info()  # 显示任务信息

            # 循环处理启用/禁用切换
            while True:
                if self.trigger and self.trigger.isRunning():
                    # 停止当前触发器
                    self.trigger.kill()
                    self._play_sound("close")
                    self.indicate("触发已禁用")
                else:
                    # 启动新触发器
                    self.trigger = Trigger(task)
                    self.trigger.start()
                    self._play_sound("open")
                    self.indicate("触发已启用")

                # 等待禁用键触发
                keyboard.wait(self.disable_key)
                # 防止快速切换
                time.sleep(0.2)

        except Exception as e:
            self.indicate("任务执行异常:连点器", log=False)
            logger.error(f"任务执行异常:连点器\n{format_exc()}")
            WindowsNotify("连点器错误", f"任务执行异常: {str(e)}")
        except SGAStop:
            raise
        finally:
            self._cleanup()

    def _validate_config(self) -> bool:
        """验证任务配置有效性"""
        # 检查禁用键
        if not self.disable_key:
            self.indicate("禁用启用键不能为空")
            return False

        # 检查触发键
        trigger_key = self.task.get("triggerkey", "").strip()
        if not trigger_key:
            self.indicate("触发键不能为空")
            return False

        # 检查连点模式配置
        clicker_mode = self.task.get("ClickerMode", "")
        if clicker_mode == "脚本模式":
            if not self._validate_script_config():
                return False
        else:
            clicker_key = self.task.get("clickerkey", "").strip()
            if not clicker_key:
                self.indicate("连击键不能为空")
                return False
            if not self._validate_clicker_keys(clicker_key):
                return False

        # 验证触发键
        return self._validate_trigger_keys(trigger_key)

    def _validate_trigger_keys(self, trigger_key: str) -> bool:
        """验证触发键有效性"""
        trigger_list = [key.strip().upper() for key in trigger_key.split("+") if key.strip()]
        has_invalid = False

        for key in trigger_list:
            if key not in TRIGGER_MOUSE_LIST and key not in TRIGGER_KEY_LIST:
                self.indicate(f"触发键包含无效键值: {key}")
                has_invalid = True

        # 检查鼠标触发键格式
        mouse_keys = [k for k in trigger_list if k in TRIGGER_MOUSE_LIST]
        if len(mouse_keys) > 1:
            self.indicate("触发键只能包含一个鼠标键")
            has_invalid = True

        return not has_invalid

    def _validate_clicker_keys(self, clicker_key: str) -> bool:
        """验证点击键有效性"""
        clicker_list = [key.strip().upper() for key in clicker_key.split("+") if key.strip()]
        mouse_keys = [k for k in clicker_list if k in CLICKER_MOUSE_LIST]

        # 鼠标键不能与其他键组合
        if len(mouse_keys) > 1 or (len(mouse_keys) == 1 and len(clicker_list) > 1):
            self.indicate("鼠标点击键不能与其他键组合")
            return False

        # 检查无效键
        for key in clicker_list:
            if key not in CLICKER_MOUSE_LIST and key not in CLICKER_KEY_LIST:
                self.indicate(f"连击键包含无效键值: {key}")
                return False

        return True

    def _validate_script_config(self) -> bool:
        """验证脚本模式配置"""
        script_name = self.task.get("scriptname", "").strip()
        if not script_name:
            self.indicate("脚本名不能为空")
            return False

        # 检查脚本文件
        sc_path = os.path.join("personal/ptscript", f"{script_name}.txt")
        if not os.path.exists(sc_path):
            self.indicate(f"脚本文件不存在: {sc_path}")
            return False

        # 解析并验证脚本内容
        try:
            with open(sc_path, 'r', encoding='utf-8') as f:
                sc_list = []
                line_num = 0
                for line in f:
                    line_num += 1
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(":", 1)
                    if len(parts) != 2:
                        self.indicate(f"脚本格式错误(行{line_num}): {line}")
                        return False

                    func_name, func_value = parts[0].strip(), parts[1].strip()
                    if func_name in ["clickdown", "clickup"]:
                        if func_value.upper() not in CLICKER_MOUSE_LIST:
                            self.indicate(f"脚本无效鼠标键(行{line_num}): {func_value}")
                            return False
                        sc_list.append([func_name, func_value])
                    elif func_name == "moveto":
                        coords = func_value.split(",")
                        if len(coords) != 2 or not all(c.strip().isdigit() for c in coords):
                            self.indicate(f"脚本坐标错误(行{line_num}): {func_value}")
                            return False
                        sc_list.append([func_name, (int(coords[0]), int(coords[1]))])
                    elif func_name in ["keydown", "keyup"]:
                        if func_value.upper() not in CLICKER_KEY_LIST:
                            self.indicate(f"脚本无效键盘键(行{line_num}): {func_value}")
                            return False
                        sc_list.append([func_name, func_value])
                    elif func_name == "wait":
                        if not func_value.isdigit():
                            self.indicate(f"脚本等待时间错误(行{line_num}): {func_value}")
                            return False
                        sc_list.append([func_name, int(func_value)])
                    else:
                        self.indicate(f"脚本未知命令(行{line_num}): {func_name}")
                        return False

                self.task["script"] = sc_list
                return True
        except Exception as e:
            self.indicate(f"脚本解析错误: {str(e)}")
            return False

    def _show_task_info(self):
        """显示任务信息"""
        tm = self.task["TriggerMode"]
        cm = self.task["ClickerMode"]
        trigger = self.task["triggerkey"]

        self.indicate("---------------")
        self.indicate(f"触发模式: {tm}")
        self.indicate(f"触发键: '{trigger}'")
        self.indicate(f"连点模式: {cm}")

        if cm == "脚本模式":
            cna = self.task["scriptname"]
            cnu = self.task["runnum"] if self.task["runnum"] > 0 else "持续"
            self.indicate(f"脚本方案名: {cna}")
            self.indicate(f"循环次数: {cnu}")
        else:
            clicker = self.task["clickerkey"]
            ct = self.task["interval"]
            self.indicate(f"连点键: '{clicker}'")
            self.indicate(f"连点间隔: {ct} ms")

        self.indicate(f"短按 '{self.disable_key}' 启用/禁用触发")
        self.indicate("---------------")

    def _play_sound(self, sound_type: str):
        """播放提示音"""
        if self.task.get("静音", False):
            return

        sound_path = f"assets/presstrigger/{sound_type}.mp3"
        try:
            playsound3.playsound(sound_path, block=False)
        except Exception as e:
            logger.warning(f"播放提示音失败: {str(e)}")

    def _cleanup(self):
        """清理资源"""
        if self.trigger and self.trigger.isRunning():
            self.trigger.kill()
        self.indicate("连点器任务已停止")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出时清理"""
        self._cleanup()