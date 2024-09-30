from qfluentwidgets import DoubleSpinBox
from ui.element.ui_part import Independent
from ui.element.control import *


class Local:
    def __init__(self, stack):
        # 初始化窗口
        self.page_local = Widget(stack)
        stack.addWidget(self.page_local)
        # 添加控件
        self.label_local = Label(self.page_local, (0, 12, 180, 18), "设置页面：环行旅舍 运行方式")
        Line(self.page_local, (0, 42, 395, 3))

        self.label_klein_overall = Label(self.page_local, (0, 50, 180, 27), "全局设置：")
        self.label_start = Label(self.page_local, (0, 90, 80, 27), "服务器")  # 启动路径 /
        self.combo_server = Combobox(self.page_local, (80, 90, 100, 32))
        self.combo_server.addItems(["官服", "B服"])
        self.label_start = Label(self.page_local, (0, 130, 80, 27), "启动路径")
        self.line_start = Lineedit(self.page_local, (0, 160, 385, 33))
        Line(self.page_local, (0, 202, 395, 3))

        self.label_team_tip = Label(self.page_local, (0, 210, 220, 27), "独立运行设置：")
        self.independent = Independent(self.page_local, (0, 250, 350, 70))
        Line(self.page_local, (0, 330, 395, 3))
        self.label_tools = Label(self.page_local, (0, 335, 220, 27), "实用工具：")
        self.button_gift = Button(self.page_local, (0, 370, 100, 30), "认可度礼物")
        self.button_wiki = Button(self.page_local, (110, 370, 85, 30), "舍友图鉴")


class Fight:
    def __init__(self, stack):
        # 初始化窗口
        self.page_fight = Widget(stack)
        stack.addWidget(self.page_fight)
        # 添加控件
        self.label_fight = Label(self.page_fight, (0, 12, 220, 18), "设置页面：作战/重游")
        self.label_mat = Label(self.page_fight, (120, 50, 80, 18), "材料选择")
        self.re_fight = Check(self.page_fight, (0, 90, 180, 18), "再次重游")
        self.mat = Combobox(self.page_fight, (110, 80, 100, 40))
        self.mat.addItems(["格", "风物志", "节"])


class Disp:
    def __init__(self, stack):
        # 初始化窗口
        self.page_dispatch = Widget(stack)
        stack.addWidget(self.page_dispatch)
        # 添加控件
        self.label_dispatch = Label(self.page_dispatch, (0, 12, 180, 18), "设置页面：探索派遣")

        self.check_redisp = Check(self.page_dispatch, (0, 50, 180, 18), "再次采购")

        self.label_disp_mat = Label(self.page_dispatch, (25, 80, 80, 27), "材料选择")
        self.label_fund = Label(self.page_dispatch, (130, 80, 80, 27), "资金选择")
        self.label_plan = Label(self.page_dispatch, (260, 80, 80, 27), "方案选择")

        self.mat0 = Combobox(self.page_dispatch, (0, 110, 100, 32))
        self.mat1 = Combobox(self.page_dispatch, (0, 150, 100, 32))
        self.mat2 = Combobox(self.page_dispatch, (0, 190, 100, 32))
        self.mat3 = Combobox(self.page_dispatch, (0, 230, 100, 32))
        self.mat4 = Combobox(self.page_dispatch, (0, 270, 100, 32))
        self.mat5 = Combobox(self.page_dispatch, (0, 310, 100, 32))

        self.fund0 = Combobox(self.page_dispatch, (115, 110, 100, 32))
        self.fund1 = Combobox(self.page_dispatch, (115, 150, 100, 32))
        self.fund2 = Combobox(self.page_dispatch, (115, 190, 100, 32))
        self.fund3 = Combobox(self.page_dispatch, (115, 230, 100, 32))
        self.fund4 = Combobox(self.page_dispatch, (115, 270, 100, 32))
        self.fund5 = Combobox(self.page_dispatch, (115, 310, 100, 32))

        self.plan0 = Combobox(self.page_dispatch, (225, 110, 140, 32))
        self.plan1 = Combobox(self.page_dispatch, (225, 150, 140, 32))
        self.plan2 = Combobox(self.page_dispatch, (225, 190, 140, 32))
        self.plan3 = Combobox(self.page_dispatch, (225, 230, 140, 32))
        self.plan4 = Combobox(self.page_dispatch, (225, 270, 140, 32))
        self.plan5 = Combobox(self.page_dispatch, (225, 310, 140, 32))

        mat_list = ["食油", "黄油", "生抽", "食盐", "胡椒", "酱料", "糖类", "芥末", "香料粉", "西红柿醋"]
        self.mat0.addItems(mat_list)
        self.mat1.addItems(mat_list)
        self.mat2.addItems(mat_list)
        self.mat3.addItems(mat_list)
        self.mat4.addItems(mat_list)
        self.mat5.addItems(mat_list)

        fund_list = ["零元购", "1000格", "2000格", "3000格"]
        self.fund0.addItems(fund_list)
        self.fund1.addItems(fund_list)
        self.fund2.addItems(fund_list)
        self.fund3.addItems(fund_list)
        self.fund4.addItems(fund_list)
        self.fund5.addItems(fund_list)

        plan_list = ["更多固定物品", "更多额外物品", "减少采购时间"]
        self.plan0.addItems(plan_list)
        self.plan1.addItems(plan_list)
        self.plan2.addItems(plan_list)
        self.plan3.addItems(plan_list)
        self.plan4.addItems(plan_list)
        self.plan5.addItems(plan_list)


class Review:
    def __init__(self, stack):
        # 初始化窗口
        self.page_review = Widget(stack)
        stack.addWidget(self.page_review)
        # 添加控件
        self.label_review = Label(self.page_review, (0, 12, 200, 18), "设置页面：战术回顾")

        self.label_review_choose = Label(self.page_review, (0, 50, 100, 18), "战术回顾选择")
        self.num_box_review = DoubleSpinBox(self.page_review)
        self.num_box_review.setGeometry(QtCore.QRect(0, 80, 160, 30))


class Market:
    def __init__(self, stack):
        # 初始化窗口
        self.page_market = Widget(stack)
        stack.addWidget(self.page_market)
        # 添加控件
        self.label_recruit = Label(self.page_market, (0, 12, 180, 18), "设置页面：集市领取")
        self.check_mconvert = Check(self.page_market, (0, 85, 100, 22), "援外兑换")
        self.box_mconvert = Combobox(self.page_market, (105, 80, 180, 32))
        self.box_mconvert.addItems(["须臾", "原液", "燧石矿物", "磁片",
                                    "翼片", "古语石", "固醇粒", "异态水",
                                    "甜品自助餐劵", "游戏机", "毛毯", "遮阳伞",
                                    "小哑铃", "爱之歌", "手握式小风扇", "演唱会门票",
                                    "相机", "灯塔胶囊"])


class Recruit:
    def __init__(self, stack):
        # 初始化窗口
        self.page_recruit = Widget(stack)
        stack.addWidget(self.page_recruit)
        # 添加控件
        self.label_recruit = Label(self.page_recruit, (0, 12, 180, 18), "设置页面：舍友访募")

        self.check_accelerate = Check(self.page_recruit, (0, 85, 80, 22), "加速")
        self.label_recruit_plan = Label(self.page_recruit, (115, 50, 80, 18), "招募计划")
        self.recruit_plan = Combobox(self.page_recruit, (105, 80, 100, 32))
        self.recruit_plan.addItems(["0格", "100格", "200格", "300格", "400格", "500格", "600格", "700格"])

        self.button_history = TransPicButton(
            self.page_recruit, (220, 45, 30, 30),
            "assets/main_window/ui/history.png", (25, 25))
        self.button_directory = TransPicButton(
            self.page_recruit, (220, 85, 30, 30),
            "assets/main_window/ui/directory.png", (25, 25))


class Reward:
    def __init__(self, stack):
        # 初始化窗口
        self.page_reward = Widget(stack)
        stack.addWidget(self.page_reward)
        # 添加控件
        self.label_recruit = Label(self.page_reward, (0, 12, 180, 18), "设置页面：今日工作")
        self.check_weekly = Check(self.page_reward, (0, 85, 120, 22), "兑换每周补给")
        self.box_weekly1 = Combobox(self.page_reward, (0, 115, 180, 32))
        self.box_weekly1.addItems(["甜品自助餐劵", "游戏机", "毛毯", "遮阳伞",
                                   "小哑铃", "爱之歌", "手握式小风扇", "演唱会门票",
                                   "相机", "灯塔胶囊"])
        self.box_weekly2 = Combobox(self.page_reward, (0, 160, 180, 32))
        self.box_weekly2.addItems(["甜品自助餐劵", "游戏机", "毛毯", "遮阳伞",
                                   "小哑铃", "爱之歌", "手握式小风扇", "演唱会门票",
                                   "相机", "灯塔胶囊"])


class Network:
    def __init__(self, stack):
        # 初始化窗口
        self.page_network = Widget(stack)
        stack.addWidget(self.page_network)
        # 添加控件
        self.label_network = Label(self.page_network, (0, 12, 180, 18), "设置页面：卡门商网")
        self.label_network_tip = Label(self.page_network, (90, 80, 220, 27), "卡门商网 暂无配置项目。")


class Mail:
    def __init__(self, stack):
        # 初始化窗口
        self.page_mail = Widget(stack)
        stack.addWidget(self.page_mail)
        # 添加控件
        self.label_mail = Label(self.page_mail, (0, 12, 180, 18), "设置页面：领取邮件")
        self.label_mail_tip = Label(self.page_mail, (90, 80, 220, 27), "领取邮件 暂无配置项目。")


class Roll:
    def __init__(self, stack):
        # 初始化窗口
        self.page_roll = Widget(stack)
        stack.addWidget(self.page_roll)
        # 添加控件
        self.label_roll = Label(self.page_roll, (0, 12, 180, 18), "设置页面：抽卡记录")
        self.button_arrange = Button(self.page_roll, (0, 45, 180, 30), "导出抽卡记录为Excel")
        self.button_open_roll = (
            TransPicButton(self.page_roll, (185, 45, 30, 30),
                           "assets/main_window/ui/directory.png", (25, 25)))
        self.label_roll_tip = Label(self.page_roll, (90, 100, 220, 27), "抽卡记录 暂无配置项目。")


class KleinStack(Local, Fight, Disp, Review, Market, Recruit, Reward, Network, Mail, Roll):
    def __init__(self, widget, location):
        # 功能堆叠窗口
        self.stack = Stack(widget, location)
        Local.__init__(self, self.stack)
        Fight.__init__(self, self.stack)
        Disp.__init__(self, self.stack)
        Review.__init__(self, self.stack)
        Market.__init__(self, self.stack)
        Recruit.__init__(self, self.stack)
        Reward.__init__(self, self.stack)
        Network.__init__(self, self.stack)
        Mail.__init__(self, self.stack)
        Roll.__init__(self, self.stack)
