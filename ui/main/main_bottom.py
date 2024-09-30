from ..module.main import Module
from ..overall.main import Overall
from .main_window import *
from json import dump, load
from tools.environment import *
from traceback import format_exc
from os import rename


# 加载主窗口和函数
class MainBottom(MainWindow, Module, Overall):
    def __init__(self):
        super().__init__()
        # 载入主窗口
        try:
            MainWindow.__init__(self)
        except Exception as err:
            message_box("主窗口加载异常(1/7):\n%s\n" % err)
            logger.critical("主窗口加载异常(1/6):\n%s\n" % format_exc())
            sys.exit(1)
        # 载入全局设置窗口
        try:
            self.overall = Overall(self.stack_setting)
        except Exception as err:
            message_box("全局设置窗口加载失败(2/7):\n%s\n" % err)
            logger.critical("全局设置窗口加载失败(2/7):\n%s\n" % format_exc())
            sys.exit(1)
        # 载入模组设置窗口
        try:
            Module.__init__(self, self)
        except Exception as err:
            message_box("模组设置窗口加载失败(3/7):\n%s\n" % err)
            logger.critical("模组设置窗口加载失败(3/7):\n%s\n" % format_exc())
            sys.exit(1)

    # 切换页面
    def change_interface(self):
        if self.state["stack"]:
            self.stack_setting.setCurrentIndex(0)
            self.state["stack"] = 0
        else:
            self.stack_setting.setCurrentIndex(1)
            self.state["stack"] = 1

    # 设置锁定模式
    def set_lock(self, mode):
        if mode:
            self.button_config_unlock.hide()
            self.button_config_lock.show()
        else:
            self.button_config_lock.hide()
            self.button_config_unlock.show()
        self.state["locked"] = mode

    # 配置重命名
    def config_rename(self):
        text_past = self.state["text"]
        text_now = self.box_config_change.currentText()
        prefix = self.state["plan"][text_past]
        new_path = r"personal/config/%s.json" % (prefix + text_now)
        if text_now == text_past:
            pass
        elif text_now in self.state["plan"]:
            self.indicate("配置名重复：请键入其他名字", 3)
            self.box_config_change.setCurrentText(text_past)
        else:
            rename(r"personal/config/%s.json" % (prefix + text_past), new_path)
            self.overall.timer.overall_rename_item(text_past, text_now)
            if prefix != "00" and self.state["mix"]["load"]:
                self.mix.rename_item(text_past, text_now)
            self.state["plan"][text_now] = self.state["plan"].pop(text_past)
            self.state["text"] = text_now
            self.indicate("配置更名：%s >>> %s" % (text_past, text_now), 3)

    # （加载并）切换模组设置页面
    def change_module(self, num):
        name_list = self.state["name"]
        name = name_list[num]
        if not self.state[name]["load"]:
            module = eval(f"self.{name}")
            module.load_window()
            if num == 0:
                module.load_single(self.state["single"])
            elif num < len(name_list):
                module.load_run(self.config[name])
            self.state[name]["load"] = True
        else:
            pass
        self.stack_module.setCurrentIndex(num)

    def get_file_path(self, text):
        return "personal/config/%s.json" % (self.state["plan"][text] + text)

    def get_config_dir(self, text="current"):
        if text == "current":
            _num = self.stack_module.currentIndex()
            _text = self.state["name"][_num]
            module = eval(f"self.{_text}")
            config_dir = module.output_config()
        else:
            with open(self.get_file_path(text), 'r', encoding='utf-8') as c:
                config_dir = load(c)
        return config_dir

    # 根据字典载入面板/根据字典和名称保存配置至文件
    def send_config_dir(self, dictionary, text="current"):
        if text == "current":
            _num = dictionary["模块"]
            self.change_module(_num)
            _text = self.state["name"][_num]
            module = eval(f"self.{_text}")
            module.input_config(dictionary)
        else:
            with open(self.get_file_path(text), 'w', encoding='utf-8') as c:
                dump(dictionary, c, ensure_ascii=False, indent=1)

    # 显示声明
    def show_statement(self):
        note = "使用须知:\n" \
               "    1、该项目（以下称SGA）免费、开源。如果您付费购买了该工具，请申请退款并举报售卖方，每一次倒卖都会使开源更加困难。\n" \
               "    2、SGA包含第三方工具模块，所有第三方工具都不保证没有封号风险，怕别用，封认罚。\n" \
               "    3、SGA更新随缘。警告维权，问题反馈，SGA更新，合作建议，请关注B站账号:绘星痕。\n" \
               "    4、模块运行期间，可点击界面上“停止”按钮或键盘组合键“ctrl+/”快捷中止运行。\n" \
               "    5、卸载/删除SGA前请“清除定时”，否则您的电脑可能仍会出现“睡眠”状态中自启的情况。\n" \
               "    6、关于SGA使用方法和项目详情，可查看SGA文件夹中的说明文件的详细说明，" \
               "和SGA各子界面的帮助按钮的精简提示，或参考B站账号:绘星痕 的SGA介绍和演示视频。\n" \
               "------------------------------"
        self.box_info.append(note)
