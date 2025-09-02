from maincode.tools.sgaqt.texts import Label, tips
from maincode.tools.sgaqt.buttons import Button, Check, Combobox, Timepicker
from maincode.tools.sgaqt.widgets import Widget, ScrollArea

# 常量定义
EXECUTE_COMBO_WIDTH = 90
EXECUTE_COMBO_HEIGHT = 30
TIMER_PICKER_WIDTH = 50
TIMER_PICKER_HEIGHT = 30
TEXT_COMBO_WIDTH = 210
TEXT_COMBO_HEIGHT = 30
CHECK_WIDTH = 30
CHECK_HEIGHT = 30

ITEM_COUNT = 10  # 可配置项数


class TimerWidgets(Widget):
    def __init__(self, widget, location: (int, int, int, int)):
        super().__init__(widget, location)
        # 时间条目控制
        self.lbitemchange = Label(self, (0, 0, 100, 30), "定时任务：")
        self.btdelete = Button(self, (540, 0, 80, 30), "清除定时")
        tips(self.btdelete, "取消SGA自启和唤醒行为")

        # 时间条目标签
        self.lbexecute = Label(self, (35, 30, 50, 30), "执行")
        self.lbtimer = Label(self, (205, 30, 50, 30), "定时")
        self.lbtext = Label(self, (415, 30, 80, 30), "配置选择")
        self.lbawake = Label(self, (565, 30, 60, 30), "唤醒")
        # 时间条目列表
        self.sratime = ScrollArea(self, (0, 65, 620, 120))
        self.wdtime = TimerWidget(self, (0, 0, 620, 120))
        self.sratime.setWidget(self.wdtime)


class TimerWidget(Widget):
    def __init__(self, widget: Widget, loc):
        super().__init__(widget, loc)
        self.setFixedHeight(400)

        # 初始化控件容器
        self.executes = []
        self.timers = []
        self.texts = []
        self.awakes = []

        # 创建控件
        self._create_controls()

    def _create_controls(self):
        execute_list = ["禁用", "每日", "周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        y_offset = 5
        y_step = 40

        for i in range(ITEM_COUNT):
            y_pos = y_offset + i * y_step

            # 执行下拉框
            execute = Combobox(self, (5, y_pos, EXECUTE_COMBO_WIDTH, EXECUTE_COMBO_HEIGHT))
            execute.addItems(execute_list)
            self.executes.append(execute)

            # 时间选择器
            timer = Timepicker(self, (100, y_pos, TIMER_PICKER_WIDTH, TIMER_PICKER_HEIGHT))
            self.timers.append(timer)

            # 配置选择下拉框
            text = Combobox(self, (345, y_pos, TEXT_COMBO_WIDTH, TEXT_COMBO_HEIGHT))
            self.texts.append(text)

            # 唤醒复选框
            awake = Check(self, (570, y_pos, CHECK_WIDTH, CHECK_HEIGHT), " ")
            self.awakes.append(awake)
