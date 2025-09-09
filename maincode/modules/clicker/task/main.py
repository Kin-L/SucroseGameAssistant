import time
import os
import keyboard
import playsound3
from maincode.tools.system.notification import GetTracebackInfo
from maincode.tools.core.baseclass import SGAStop
from maincode.tools.core.logger import logger
from .trigger import Trigger, TRIGGER_MOUSE_LIST

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


def taskstart(self):
    """启动触发任务"""
    self.disable_key = self.para.get("DisableKey", "").strip()
    self.trigger = None
    self.switch = False
    # 验证配置有效性
    if not _validate_config(self):
        return 0

    # 初始化并启动触发器
    try:
        _show_task_info(self)  # 显示任务信息

        def on_press(event):
            if self.trigger and self.trigger.isRunning():
                # 停止当前触发器
                self.trigger.kill()
                _play_sound("close")
                self.send("触发已禁用")
            else:
                # 启动新触发器
                self.trigger = Trigger(self.para)
                self.trigger.start()
                _play_sound("open")
                self.send("触发已启用")

        self.keyboard_listener = keyboard.on_press_key(self.disable_key, on_press)
        # 循环处理启用/禁用切换
        while True:
            self.ctler.wait(0.4)

    except Exception as e:
        self.send("任务执行异常:连点器")
        logger.error(f"{GetTracebackInfo(e)}任务执行异常:连点器")
    except SGAStop:
        raise
    finally:
        _cleanup(self)


def _validate_config(self) -> bool:
    """验证任务配置有效性"""
    # 检查禁用键
    if not self.disable_key:
        self.send("禁用启用键不能为空")
        return False

    # 检查触发键
    trigger_key = self.para.get("TriggerKey", "").strip()
    if not trigger_key:
        self.send("触发键不能为空")
        return False

    # 检查连点模式配置
    clicker_mode = self.para.get("ClickerMode", "")
    if clicker_mode != "脚本模式":
        clicker_key = self.para.get("ClickerKey", "").strip()
        if not clicker_key:
            self.send("连击键不能为空")
            return False
        if not _validate_clicker_keys(self, clicker_key):
            return False
    else:
        self.send("脚本模式开发未完成")
        return False
        # if not _validate_script_config(self):
        #     return False
    # 验证触发键
    return _validate_trigger_keys(self, trigger_key)


def _validate_trigger_keys(self, trigger_key: str) -> bool:
    """验证触发键有效性"""
    trigger_list = [key.strip().upper() for key in trigger_key.split("+") if key.strip()]
    has_invalid = False

    for key in trigger_list:
        if key not in TRIGGER_MOUSE_LIST and key not in TRIGGER_KEY_LIST:
            self.send(f"触发键包含无效键值: {key}")
            has_invalid = True

    # 检查鼠标触发键格式
    mouse_keys = [k for k in trigger_list if k in TRIGGER_MOUSE_LIST]
    if len(mouse_keys) > 1:
        self.send("触发键只能包含一个鼠标键")
        has_invalid = True

    return not has_invalid


def _validate_clicker_keys(self, clicker_key: str) -> bool:
    """验证点击键有效性"""
    clicker_list = [key.strip().upper() for key in clicker_key.split("+") if key.strip()]
    mouse_keys = [k for k in clicker_list if k in CLICKER_MOUSE_LIST]

    # 鼠标键不能与其他键组合
    if len(mouse_keys) > 1 or (len(mouse_keys) == 1 and len(clicker_list) > 1):
        self.send("鼠标点击键不能与其他键组合")
        return False

    # 检查无效键
    for key in clicker_list:
        if key not in CLICKER_MOUSE_LIST and key not in CLICKER_KEY_LIST:
            self.send(f"连击键包含无效键值: {key}")
            return False

    return True


def _validate_script_config(self) -> bool:
    """验证脚本模式配置"""
    script_name = self.para.get("scriptname", "").strip()
    if not script_name:
        self.send("脚本名不能为空")
        return False

    # 检查脚本文件
    sc_path = os.path.join("personal/ptscript", f"{script_name}.txt")
    if not os.path.exists(sc_path):
        self.send(f"脚本文件不存在: {sc_path}")
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
                    self.send(f"脚本格式错误(行{line_num}): {line}")
                    return False

                func_name, func_value = parts[0].strip(), parts[1].strip()
                if func_name in ["clickdown", "clickup"]:
                    if func_value.upper() not in CLICKER_MOUSE_LIST:
                        self.send(f"脚本无效鼠标键(行{line_num}): {func_value}")
                        return False
                    sc_list.append([func_name, func_value])
                elif func_name == "moveto":
                    coords = func_value.split(",")
                    if len(coords) != 2 or not all(c.strip().isdigit() for c in coords):
                        self.send(f"脚本坐标错误(行{line_num}): {func_value}")
                        return False
                    sc_list.append([func_name, (int(coords[0]), int(coords[1]))])
                elif func_name in ["keydown", "keyup"]:
                    if func_value.upper() not in CLICKER_KEY_LIST:
                        self.send(f"脚本无效键盘键(行{line_num}): {func_value}")
                        return False
                    sc_list.append([func_name, func_value])
                elif func_name == "wait":
                    if not func_value.isdigit():
                        self.send(f"脚本等待时间错误(行{line_num}): {func_value}")
                        return False
                    sc_list.append([func_name, int(func_value)])
                else:
                    self.send(f"脚本未知命令(行{line_num}): {func_name}")
                    return False

            self.para["script"] = sc_list
            return True
    except Exception as e:
        self.send(f"脚本解析错误: {str(e)}")
        return False


def _show_task_info(self):
    """显示任务信息"""
    tm = self.para["TriggerMode"]
    cm = self.para["ClickerMode"]
    trigger = self.para["TriggerKey"]

    self.send("---------------")
    self.send(f"触发模式: {tm}")
    self.send(f"触发键: '{trigger}'")
    self.send(f"连点模式: {cm}")

    if cm == "脚本模式":
        cna = self.para["ScriptName"]
        cnu = self.para["RunNum"] if self.para["RunNum"] > 0 else "持续"
        self.send(f"脚本方案名: {cna}")
        self.send(f"循环次数: {cnu}")
    else:
        clicker = self.para["ClickerKey"]
        ct = self.para["Interval"]
        self.send(f"连点键: '{clicker}'")
        self.send(f"连点间隔: {ct} ms")

    self.send(f"短按 '{self.disable_key}' 启用/禁用触发")
    self.send("---------------")


def _play_sound(sound_type: str):
    sound_path = f"resources/clicker/{sound_type}.mp3"
    try:
        playsound3.playsound(sound_path, block=False)
    except Exception as e:
        logger.warning(f"播放提示音失败: {str(e)}")


def _cleanup(self):
    """清理资源"""
    if self.trigger and self.trigger.isRunning():
        self.trigger.kill()
    keyboard.unhook(self.keyboard_listener)
    self.send("连点器任务已停止")
