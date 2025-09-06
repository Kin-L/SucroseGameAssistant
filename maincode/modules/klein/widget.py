from typing import Optional
from qfluentwidgets import DoubleSpinBox
from maincode.modules.template import ModuleStackPage
from maincode.tools.sgaqt.buttons import Check, Combobox, SetButton, TransPicButton, Button
from maincode.tools.sgaqt.texts import Label, SLineEdit, Line, Picture
from maincode.tools.sgaqt.widgets import Widget, SetStackPage, TaskPanel
from PyQt5 import QtCore


class KleinPage(ModuleStackPage):
    def __init__(self):
        super().__init__()
        self.wdlist: Optional[KleinList] = None
        self.page00: Optional[KleinPage00Set] = None
        self.page01: Optional[KleinPage01Set] = None
        self.page02: Optional[KleinPage02Set] = None
        self.page03: Optional[KleinPage03Set] = None
        self.page04: Optional[KleinPage04Set] = None
        self.page05: Optional[KleinPage05Set] = None
        self.page06: Optional[KleinPage06Set] = None
        self.page07: Optional[KleinPage07Set] = None
        self.page08: Optional[KleinPage08Set] = None
        self.page09: Optional[KleinPage09Set] = None
        self.picbt: Optional[Picture] = None
        self.pbset00 = SetButton(self, (180, 10, 25, 25), (25, 25))

    def LoadWidget(self):
        # 初始化功能列表
        self.wdlist = KleinList()
        self.srlist.setWidget(self.wdlist)

        # 初始化设置页面
        self.page00 = KleinPage00Set()  # 基础配置
        self.page01 = KleinPage01Set()  # 作战相关
        self.sksetting.addWidget(self.page00)
        self.sksetting.addWidget(self.page01)

        # 分隔线
        Line(self, (215, 5, 3, 530), False)

        # 绑定页面切换事件
        self.wdlist.set_klein.clicked.connect(lambda: self.sksetting.setCurrentIndex(0))
        self.wdlist.set_fight.clicked.connect(lambda: self.sksetting.setCurrentIndex(1))
        # 其他页面切换绑定...

    def SetWidget(self, config: dict):
        ...

    def CollectConfig(self) -> dict:
        return {}


class KleinList(Widget):
    def __init__(self):
        super().__init__()
        self.ckitem01 = Check(self, (0,   5, 120, 22), "作战/重游")
        self.ckitem02 = Check(self, (0,  50, 120, 22), "线下采购")
        self.ckitem03 = Check(self, (0,  95, 120, 22), "战术回顾")
        self.ckitem04 = Check(self, (0, 140, 120, 22), "集市领取")
        self.lbitem05 = Check(self, (0, 185, 120, 22), "舍友访募")
        self.lbitem06 = Check(self, (0, 230, 120, 22), "今日工作")
        self.lbitem07 = Check(self, (0, 275, 120, 22), "卡门商网")
        self.lbitem08 = Check(self, (0, 320, 120, 22), "领取邮件")
        self.lbitem09 = Check(self, (0, 365, 120, 22), "抽卡历史")

        self.pbset01 = SetButton(self, (175,   5, 25, 25), (25, 25))
        self.pbset02 = SetButton(self, (175,  50, 25, 25), (25, 25))
        self.pbset03 = SetButton(self, (175,  95, 25, 25), (25, 25))
        self.pbset04 = SetButton(self, (175, 140, 25, 25), (25, 25))
        self.pbset05 = SetButton(self, (175, 185, 25, 25), (25, 25))
        self.pbset06 = SetButton(self, (175, 230, 25, 25), (25, 25))
        self.pbset07 = SetButton(self, (175, 275, 25, 25), (25, 25))
        self.pbset08 = SetButton(self, (175, 320, 25, 25), (25, 25))
        self.pbset09 = SetButton(self, (175, 365, 25, 25), (25, 25))


class KleinPage00Set(SetStackPage):
    """全局设置页面"""

    def __init__(self):
        super().__init__("设置页面：运行方式")

        # 全局设置区域
        Label(self.page, (0, 50, 180, 27), "全局设置：")
        Label(self.page, (0, 90, 80, 27), "服务器")
        self.combo_server = Combobox(self.page, (80, 90, 100, 32))
        self.combo_server.addItems(["官服", "B服"])

        Label(self.page, (0, 130, 80, 27), "启动路径")
        self.lepath = SLineEdit(self, (0, 160, 385, 33))
        Line(self.page, (0, 202, 395, 3))

        # 独立运行设置
        self.taskpanel = TaskPanel(self, 210)

        # 实用工具
        Label(self.page, (0, 335, 220, 27), "实用工具：")
        self.button_gift = Button(self.page, (0, 370, 100, 30), "认可度礼物")
        self.button_wiki = Button(self.page, (110, 370, 85, 30), "舍友图鉴")


class KleinPage01Set(SetStackPage):
    """作战/重游设置页面"""

    def __init__(self):
        super().__init__("设置页面：作战/重游")
        Label(self.page, (120, 50, 80, 18), "材料选择")

        self.re_fight = Check(self.page, (0, 90, 180, 18), "再次重游")
        self.mat = Combobox(self.page, (110, 80, 100, 40))
        self.mat.addItems(["格", "风物志", "节"])


class KleinPage02Set(SetStackPage):
    """探索派遣设置页面"""

    def __init__(self):
        super().__init__("设置页面：探索派遣")
        self.check_redisp = Check(self.page, (0, 50, 180, 18), "再次采购")

        # 表头
        Label(self.page, (25, 80, 80, 27), "材料选择")
        Label(self.page, (130, 80, 80, 27), "资金选择")
        Label(self.page, (260, 80, 80, 27), "方案选择")

        # 材料选择下拉框
        mat_list = ["食油", "黄油", "生抽", "食盐", "胡椒", "酱料", "糖类", "芥末", "香料粉", "西红柿醋"]
        self.mat_boxes = [
            Combobox(self.page, (0, 110, 100, 32)),
            Combobox(self.page, (0, 150, 100, 32)),
            Combobox(self.page, (0, 190, 100, 32)),
            Combobox(self.page, (0, 230, 100, 32)),
            Combobox(self.page, (0, 270, 100, 32)),
            Combobox(self.page, (0, 310, 100, 32)),
        ]
        for box in self.mat_boxes:
            box.addItems(mat_list)

        # 资金选择下拉框
        fund_list = ["零元购", "1000格", "2000格", "3000格"]
        self.fund_boxes = [
            Combobox(self.page, (115, 110, 100, 32)),
            Combobox(self.page, (115, 150, 100, 32)),
            Combobox(self.page, (115, 190, 100, 32)),
            Combobox(self.page, (115, 230, 100, 32)),
            Combobox(self.page, (115, 270, 100, 32)),
            Combobox(self.page, (115, 310, 100, 32)),
        ]
        for box in self.fund_boxes:
            box.addItems(fund_list)

        # 方案选择下拉框
        plan_list = ["更多固定物品", "更多额外物品", "减少采购时间"]
        self.plan_boxes = [
            Combobox(self.page, (225, 110, 140, 32)),
            Combobox(self.page, (225, 150, 140, 32)),
            Combobox(self.page, (225, 190, 140, 32)),
            Combobox(self.page, (225, 230, 140, 32)),
            Combobox(self.page, (225, 270, 140, 32)),
            Combobox(self.page, (225, 310, 140, 32)),
        ]
        for box in self.plan_boxes:
            box.addItems(plan_list)


class KleinPage03Set(SetStackPage):
    """战术回顾设置页面"""

    def __init__(self):
        super().__init__("设置页面：战术回顾")
        Label(self.page, (0, 50, 100, 18), "战术回顾选择")

        self.num_box_review = DoubleSpinBox(self.page)
        self.num_box_review.setGeometry(QtCore.QRect(0, 80, 160, 30))


class KleinPage04Set(SetStackPage):
    """集市领取设置页面"""

    def __init__(self):
        super().__init__("设置页面：集市领取")
        self.check_mconvert = Check(self.page, (0, 85, 100, 22), "援外兑换")

        self.box_mconvert = Combobox(self.page, (105, 80, 180, 32))
        self.box_mconvert.addItems([
            "须臾", "原液", "燧石矿物", "磁片", "翼片", "古语石",
            "固醇粒", "异态水", "甜品自助餐劵", "游戏机", "毛毯",
            "遮阳伞", "小哑铃", "爱之歌", "手握式小风扇", "演唱会门票",
            "相机", "灯塔胶囊"
        ])


class KleinPage05Set(SetStackPage):
    """舍友访募设置页面"""

    def __init__(self):
        super().__init__("设置页面：舍友访募")
        self.check_accelerate = Check(self.page, (0, 85, 80, 22), "加速")

        Label(self.page, (115, 50, 80, 18), "招募计划")
        self.recruit_plan = Combobox(self.page, (105, 80, 100, 32))
        self.recruit_plan.addItems([f"{i}00格" for i in range(8)])

        # 历史记录按钮
        self.button_history = TransPicButton(
            self.page, (220, 45, 30, 30),
            "assets/main_window/ui/history.png", (25, 25))
        self.button_directory = TransPicButton(
            self.page, (220, 85, 30, 30),
            "assets/main_window/ui/directory.png", (25, 25))


class KleinPage06Set(SetStackPage):
    """今日工作设置页面"""

    def __init__(self):
        super().__init__("设置页面：今日工作")
        self.check_weekly = Check(self.page, (0, 85, 120, 22), "兑换每周补给")

        self.box_weekly1 = Combobox(self.page, (0, 115, 180, 32))
        self.box_weekly2 = Combobox(self.page, (0, 160, 180, 32))
        week_list = ["甜品自助餐劵", "游戏机", "毛毯", "遮阳伞",
                     "小哑铃", "爱之歌", "手握式小风扇", "演唱会门票",
                     "相机", "灯塔胶囊"]
        self.box_weekly1.addItems(week_list)
        self.box_weekly2.addItems(week_list)


class KleinPage07Set(SetStackPage):
    """卡门商网设置页面"""

    def __init__(self):
        super().__init__("设置页面：卡门商网")
        Label(self.page, (90, 80, 220, 27), "卡门商网 暂无配置项目。")


class KleinPage08Set(SetStackPage):
    """领取邮件设置页面"""

    def __init__(self):
        super().__init__("设置页面：领取邮件")
        Label(self.page, (90, 80, 220, 27), "领取邮件 暂无配置项目。")


class KleinPage09Set(SetStackPage):
    """抽卡记录设置页面"""

    def __init__(self):
        super().__init__("设置页面：抽卡记录")
        self.button_arrange = Button(self.page, (0, 45, 180, 30), "导出抽卡记录为Excel")
        self.button_open_roll = TransPicButton(
            self.page, (185, 45, 30, 30),
            "assets/main_window/ui/directory.png", (25, 25))
        Label(self.page, (90, 100, 220, 27), "抽卡记录 暂无配置项目。")
