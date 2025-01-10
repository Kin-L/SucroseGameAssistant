import time
from .trigger import *
import playsound3
from ..default_task import Task
from tools.environment import *
from traceback import format_exc

trigger_mouse_list = ["LCLICK", "RCLICK", "MCLICK", 'X1CLICK', 'X2CLICK']
trigger_key_list = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",
                    "F9", "F10", "F11", "F12", "F13", "F14", "F15", "F16",
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
                    "PRINTSCREEN", "VOLUMEMUTE", "DECIMAL",
                    "[", "]", "+", "-", "~", "`", "/", ',', '.', "\\", "'", ";", "*"
                    ]
clicker_mouse_list = ["LCLICK", "RCLICK", "MCLICK"]
clicker_key_list = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",
                    "F9", "F10", "F11", "F12", "F13", "F14", "F15", "F16",
                    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                    "U", "V", "W", "X", "Y", "Z",
                    "SHIFT", "CTRL", "ALT", "WINDOWS",
                    "ENTER", "TAB", "BACKSPACE",
                    "LEFT", "UP", "RIGHT", "DOWN", "PAGEUP", "PAGEDOWN", "END", "HOME",
                    "CAPSLOCK", "ESC", "NUMLOCK", "PAUSE", "SPACE", "INSERT", "DELETE",
                    "PRINTSCREEN", "VOLUMEMUTE", "DECIMAL",
                    "[", "]", "+", "-", "~", "`", "/", ',', '.', "\\", "'", ";", "*"
                    ]


class TaskTrigger(Task):
    def __init__(self):
        super(TaskTrigger, self).__init__()
        self.trigger = None
        self.switch = False

    def trigger_start(self, task: type[dir]):
        _k = False
        self.task = task
        self.trigger = Trigger(task)
        self.indicate("开始任务:连点器")
        env.mode(2)
        tm = self.task["TriggerMode"]
        cm = self.task["ClickerMode"]
        cna = self.task["scriptname"]
        cnu = self.task["runnum"]
        ct = self.task["interval"]
        disable = self.task["disablekey"]
        trigger = self.task["triggerkey"]
        clicker = self.task["clickerkey"]
        if not disable:
            self.indicate(f"禁用启用键 不能为空")
            return 0
        if not trigger:
            self.indicate(f"触发键 不能为空")
            return 0
        false_flag = False

        disable_list = disable.strip(" ").upper().split("+")
        for i in disable_list:
            i.strip(" ")
            if i not in trigger_key_list:
                self.indicate(f"禁用启用键 无效键值：{disable}")
                false_flag = True
                break

        trigger_list = trigger.strip(" ").upper().split("+")
        trigger_click = 0
        for i in trigger_list:
            i.strip(" ")
            if i in trigger_mouse_list:
                trigger_click = i
            elif i in trigger_key_list:
                pass
            else:
                self.indicate(f"触发键 无效键值：{trigger}")
                false_flag = True
                break
        if trigger_click:
            if len(trigger_list) > 2:
                self.indicate(f"触发键 无效键值：{trigger}")
                false_flag = True
            elif trigger_list[0] in trigger_key_list+trigger_mouse_list:
                pass
            else:
                self.indicate(f"触发键 无效键值：{trigger}")
                false_flag = True

        if self.task["ClickerMode"] == "脚本模式":
            if not self.task["script_name"]:
                self.indicate(f"无效脚本名")
                return 0
            script_name = self.task["script_name"]
            sc_path = f"personal/ptscript/{script_name}.txt"
            if os.path.exists(sc_path):
                txt = open(sc_path, 'r', encoding='utf-8')
                sc_list = []
                while 1:
                    _line = txt.readline().strip("\n").strip(" ")
                    if _line:
                        _list = _line.split(":")
                        if len(_list) == 2:
                            func_name = _list[0].strip(" ")
                            func_value = _list[1].strip(" ")
                            if func_name in ["clickdown", "clickup"]:
                                if func_value in clicker_mouse_list:
                                    sc_list += [[func_name, func_value]]
                                    continue
                            elif func_name == "moveto":
                                value_list = func_value.split(",")
                                if len(value_list) == 2:
                                    if value_list[0].isdigit() and value_list[1].isdigit():
                                        sc_list += [[func_name, (int(value_list[0]), int(value_list[1]))]]
                                        continue
                            elif func_name in ["keydown", "keyup"]:
                                if func_value in clicker_key_list:
                                    sc_list += [[func_name, func_value]]
                                    continue
                            elif func_name == "wait":
                                if func_value.isdigit():
                                    sc_list += [[func_name, int(func_value)]]
                                    continue
                    else:
                        break
                    self.indicate(f"脚本流程存在无效数值")
                    txt.close()
                    return 0
                txt.close()
                self.task["script"] = sc_list
        else:
            if not clicker:
                self.indicate(f"连击键 不能为空")
                return 0
            clicker_list = clicker.strip(" ").upper().split("+")
            _num1, _num2, clicker_click = 0, 0, 0
            for i in clicker_list:
                i.strip(" ")
                if i in clicker_mouse_list:
                    if len(clicker_list) != 1:
                        self.indicate(f"连击键 无效键值：{clicker}")
                        false_flag = True
                elif i in clicker_key_list:
                    _num2 += 1
                else:
                    self.indicate(f"连击键 无效键值：{clicker}")
                    false_flag = True
        if false_flag:
            return 0
        self.indicate("---------------")
        self.indicate(f"触发模式: {tm}")
        self.indicate(f"触发键: '{trigger}' ")
        self.indicate(f"连点模式: {cm}")
        if cm == "脚本模式":
            if cnu > 0:
                cnu = "持续"
            self.indicate(f"脚本方案名: {cna}")
            self.indicate(f"循环次数: {cnu}'")
        else:
            self.indicate(f"连点键: '{clicker}' ")
            self.indicate(f"连点间隔: '{ct}' ms")
        self.indicate(f"短按 '{disable}' 启用/禁用触发")
        self.indicate("---------------")
        # noinspection PyBroadException
        try:
            while 1:
                if self.trigger.isRunning():
                    self.trigger.kill()
                    playsound3.playsound(r"assets\presstrigger\close.mp3")
                    self.indicate("触发已禁用")
                else:
                    self.trigger.start()
                    playsound3.playsound(r"assets\presstrigger\open.mp3")
                    self.indicate("触发已启用")
                keyboard.wait(self.task["disablekey"])
        except Exception:
            self.indicate("任务执行异常:连点器", log=False)
            logger.error("任务执行异常:连点器\n%s" % format_exc())

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.trigger.isRunning():
            self.trigger.kill()


if __name__ == '__main__':
    pass
