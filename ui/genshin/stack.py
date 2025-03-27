from qfluentwidgets import CompactSpinBox
from ui.element.ui_part import Independent
from ui.element.control import *
from webbrowser import open as weopen


class Local:
    def __init__(self, stack):
        # 初始化窗口
        self.page_local = Widget(stack)
        stack.addWidget(self.page_local)
        # 添加控件
        self.label_local = Label(self.page_local, (0, 12, 180, 18), "设置页面：原神 运行参数设置")
        self.line_local0 = Line(self.page_local, (0, 42, 395, 3))
        self.label_overall = Label(self.page_local, (0, 50, 180, 27), "全局设置：")
        self.label_start = Label(self.page_local, (0, 90, 80, 27), "服务器")
        self.combo_server = Combobox(self.page_local, (80, 90, 100, 32))
        self.combo_server.addItems(["官服", "B服"])
        self.label_start = Label(self.page_local, (0, 130, 80, 27), "启动路径")
        self.line_start = Lineedit(self.page_local, (0, 160, 385, 33))
        self.label_bgi = Label(self.page_local, (0, 195, 80, 25), "BGI路径")
        self.button_BGI = Button(self.page_local, (150, 195, 80, 25), "BGI下载")
        self.line_bgi = Lineedit(self.page_local, (0, 225, 385, 33))

        self.line_local1 = Line(self.page_local, (0, 260, 395, 3))

        self.label_single = Label(self.page_local, (0, 265, 220, 27), "独立运行设置：")
        self.independent = Independent(self.page_local, (0, 295, 350, 70))

class Run_way:
    def __init__(self, stack):
        # 初始化窗口
        self.page_way = Widget(stack)
        stack.addWidget(self.page_way)
        # 添加控件
        self.label_way = Label(self.page_way, (0, 12, 180, 18), "运行方式选择")
        self.runway0 = Combobox(self.page_way, (10, 50, 150, 30))
        self.runway0.addItems(["SGA", "BGI一条龙"])
        self.label_way_tip = Label(self.page_way, (0, 80, 400, 200),"SGA：使用SGA内代码运行\nBGI一条龙：使用BGI的一条龙功能运行,下面的设置不再生效\n                 (使用前请先配置好BGI)\n两者可搭配使用")
        

class Team:
    def __init__(self, stack):
        # 初始化窗口
        self.page_team = Widget(stack)
        stack.addWidget(self.page_team)
        # 添加控件
        self.label_team = Label(self.page_team, (0, 12, 180, 18), "设置页面：切换队伍")
        self.label_team_tip = Label(self.page_team, (0, 80, 400, 200),
                                    "第一次使用请亲手配置队伍,为SGA保留左边/上边第一个\n队伍为跑图队伍。队伍需求：\n  (1)1号位为任意成女体型角色(如丽莎,雷电将军）,武器、\n天赋、队伍共鸣不应有加速buff\n  (2)2号位为草元素主角或纳西妲,用于捕捉晶蝶的机关\n触发\n  (3)队伍中应有早柚,瑶瑶等角色,用于捕捉晶蝶。(4)四号位为法器角色，用于参量质变仪的触发（推荐芭芭拉）\n\n如使用自动秘境功能请将队伍配置在二号队伍位置")


dispatch_dir = {
    "蒙德": ["水晶矿,白银矿(1)", "水晶矿,白银矿(2)", "摩拉", "兽肉,禽肉", "禽蛋,甜甜花", "白萝卜,胡萝卜"],
    "璃月": ["水晶矿,白银矿", "摩拉1", "摩拉2", "马尾,金鱼草", "白萝卜,胡萝卜", "莲蓬,松茸"],
    "稻妻": ["摩拉1", "摩拉2", "兽肉,禽蛋", "禽肉,海草", "白萝卜,堇瓜", "甜甜花,日落果"],
    "须弥": ["摩拉", "蔷薇,苹果", "松茸,蘑菇", "禽蛋,日落果", "香辛果,胡萝卜", "墩墩桃,松果"],
    "枫丹": ["摩拉", "汐藻,蘑菇", "茉洁草,禽蛋", "久雨莲,兽肉", "泡泡桔,禽肉", "甜甜花,薄荷"],
    "纳塔": ["颗粒果,蘑菇", "兽肉,苹果", "烬芯花,白萝卜", "摩拉", "苦种,胡萝卜", "澄晶实,薄荷"]}


class Disp:
    def __init__(self, stack):
        # 初始化窗口
        self.page_dispatch = Widget(stack)
        stack.addWidget(self.page_dispatch)
        # 添加控件
        self.label_dispatch = Label(self.page_dispatch, (0, 12, 180, 18), "设置页面：探索派遣")

        self.label_area = Label(self.page_dispatch, (20, 45, 180, 27), "地区选择")
        self.label_mat = Label(self.page_dispatch, (180, 45, 180, 27), "材料选择")

        self.area0 = Combobox(self.page_dispatch, (0, 80, 100, 32))
        self.area1 = Combobox(self.page_dispatch, (0, 120, 100, 32))
        self.area2 = Combobox(self.page_dispatch, (0, 160, 100, 32))
        self.area3 = Combobox(self.page_dispatch, (0, 200, 100, 32))
        self.area4 = Combobox(self.page_dispatch, (0, 240, 100, 32))

        self.mat0 = Combobox(self.page_dispatch, (140, 80, 180, 32))
        self.mat1 = Combobox(self.page_dispatch, (140, 120, 180, 32))
        self.mat2 = Combobox(self.page_dispatch, (140, 160, 180, 32))
        self.mat3 = Combobox(self.page_dispatch, (140, 200, 180, 32))
        self.mat4 = Combobox(self.page_dispatch, (140, 240, 180, 32))

        self.area0.addItems(["蒙德", "璃月", "稻妻", "须弥", "枫丹", "纳塔"])
        self.area1.addItems(["蒙德", "璃月", "稻妻", "须弥", "枫丹", "纳塔"])
        self.area2.addItems(["蒙德", "璃月", "稻妻", "须弥", "枫丹", "纳塔"])
        self.area3.addItems(["蒙德", "璃月", "稻妻", "须弥", "枫丹", "纳塔"])
        self.area4.addItems(["蒙德", "璃月", "稻妻", "须弥", "枫丹", "纳塔"])

        self.mat0.addItems(dispatch_dir["蒙德"])
        self.mat1.addItems(dispatch_dir["蒙德"])
        self.mat2.addItems(dispatch_dir["蒙德"])
        self.mat3.addItems(dispatch_dir["蒙德"])
        self.mat4.addItems(dispatch_dir["蒙德"])

        self.area0.currentIndexChanged.connect(lambda: self.list_change(self.area0, self.mat0))
        self.area1.currentIndexChanged.connect(lambda: self.list_change(self.area1, self.mat1))
        self.area2.currentIndexChanged.connect(lambda: self.list_change(self.area2, self.mat2))
        self.area3.currentIndexChanged.connect(lambda: self.list_change(self.area3, self.mat3))
        self.area4.currentIndexChanged.connect(lambda: self.list_change(self.area4, self.mat4))
        self.area0.setCurrentIndex(0)
        self.area1.setCurrentIndex(0)
        self.area2.setCurrentIndex(0)
        self.area3.setCurrentIndex(0)
        self.area4.setCurrentIndex(0)
        self.mat0.setCurrentIndex(0)
        self.mat1.setCurrentIndex(0)
        self.mat2.setCurrentIndex(0)
        self.mat3.setCurrentIndex(0)
        self.mat4.setCurrentIndex(0)

        self.redisp = Check(self.page_dispatch, (0, 285, 100, 25), "再次派遣")

    @staticmethod
    def list_change(fa, fm):
        fm.clear()
        fm.addItems(dispatch_dir[fa.currentText()])


class Trans:
    def __init__(self, stack):
        # 初始化窗口
        self.page_trans = Widget(stack)
        stack.addWidget(self.page_trans)
        # 添加控件
        self.label_trans = Label(self.page_trans, (0, 12, 200, 18), "设置页面：参量质变仪")
        self.meterial_choose = Label(self.page_trans, (0, 35, 400, 40), "材料选择（先用第一种，用完了补充第二种，一种材料\n先消耗低品质的，再消耗高品质的）")
        self.meterial_choose1 = Combobox(self.page_trans, (0, 80, 160, 30))
        self.meterial_choose2 = Combobox(self.page_trans, (180, 80, 160, 30))
        self.meterial_choose1.addItems(trans_meterials)
        self.meterial_choose2.addItems(trans_meterials)
        self.team_tip = Label(self.page_trans, (0, 150, 350, 18), "请确保1号队的四号位为法器角色")
        self.meterial_tip = Label(self.page_trans, (0, 450, 350, 18), "更多材料选择请联系作者")

trans_meterials=["未选择","牛头人号角","愚人众徽记","丘丘人面具","盗宝团鸦印","史莱姆凝液"]

class Fly:
    def __init__(self, stack):
        # 初始化窗口
        self.page_fly = Widget(stack)
        stack.addWidget(self.page_fly)
        # 添加控件
        self.label_fly = Label(self.page_fly, (0, 12, 180, 18), "设置页面：自动晶蝶")
        self.fly0 = Check(self.page_fly, (0, 45, 140, 50), "雨林化城郭左方\n沙漠活力之家下方")
        self.fly1 = Check(self.page_fly, (0, 110, 140, 22), "沙漠阿如村上方")
        self.fly2 = Check(self.page_fly, (0, 165, 140, 22), "沙漠舍身陷坑下方")
        self.fly3 = Check(self.page_fly, (0, 220, 140, 22), "塔拉塔海谷")
        self.fly4 = Check(self.page_fly, (0, 275, 140, 22), "稻妻平海砦")


class Daily:
    def __init__(self, stack):
        # 初始化窗口
        self.page_Daily = Widget(stack)
        stack.addWidget(self.page_Daily)
        # 添加控件
        self.label_concentrate = Label(self.page_Daily, (0, 12, 180, 18), "设置页面：体力日常")

        self.make_condensed_resin = Check(self.page_Daily, (0, 50, 400, 25), "合成浓缩树脂")
        self.daily_gift = Check(self.page_Daily, (0, 75, 400, 25), "领取凯瑟琳每日任务奖励")

        self.hid_domain = Check(self.page_Daily, (0, 100, 180, 18), "启用秘境")

        self.label_domain_select = Label(self.page_Daily, (0, 210, 180, 18), "秘境选择")
        self.domain_type = Combobox(self.page_Daily, (0, 235, 130, 50))
        self.domain = Combobox(self.page_Daily, (140, 235, 240, 50))
        self.artifact_break = Check(self.page_Daily, (0, 290, 400, 25), "分解圣遗物（打完圣遗物秘境后）")

        self.domain_type.addItems(["圣遗物", "天赋培养素材", "武器突破素材"])
        self.domain.addItems(domain_dir["圣遗物"])

        self.domain_type.currentIndexChanged.connect(lambda: self.domain_change(self.domain_type, self.domain))
        self.button_BGI.clicked.connect(self.open_BGI)

    @staticmethod
    def domain_change(fa, fm):
        fm.clear()
        fm.addItems(domain_dir[fa.currentText()])

    @staticmethod
    def open_BGI():
        weopen.open("https://bgi.huiyadan.com/")



class Pot:
    def __init__(self, stack):
        # 初始化窗口
        self.page_pot = Widget(stack)
        stack.addWidget(self.page_pot)
        # 添加控件
        self.label_pot = Label(self.page_pot, (0, 12, 180, 18), "设置页面：尘歌壶")
        self.label_pot_tip = Label(self.page_pot, (90, 80, 220, 27), "尘歌壶 暂无配置项目。")


class Mail:
    def __init__(self, stack):
        # 初始化窗口
        self.page_mail = Widget(stack)
        stack.addWidget(self.page_mail)
        # 添加控件
        self.label_mail = Label(self.page_mail, (0, 12, 180, 18), "设置页面：领取邮件")
        self.label_mail_tip = Label(self.page_mail, (90, 80, 220, 27), "领取邮件 暂无配置项目。")


class Tree:
    def __init__(self, stack):
        # 初始化窗口
        self.page_tree = Widget(stack)
        stack.addWidget(self.page_tree)
        # 添加控件
        self.label_tree = Label(self.page_tree, (0, 12, 180, 18), "设置页面：自动伐木")
        self.CompactSpinBox = CompactSpinBox(self.page_tree)
        self.CompactSpinBox.setGeometry(QtCore.QRect(0, 40, 120, 30))

        self.tree0 = Check(self.page_tree, (0, 90, 120, 22), "桦木")
        self.tree1 = Check(self.page_tree, (130, 90, 120, 22), "萃华木")
        self.tree2 = Check(self.page_tree, (260, 90, 120, 22), "松木")
        self.tree3 = Check(self.page_tree, (0, 135, 120, 22), "却砂木")
        self.tree4 = Check(self.page_tree, (130, 135, 120, 22), "竹节")
        self.tree5 = Check(self.page_tree, (260, 135, 120, 22), "垂香木")
        self.tree6 = Check(self.page_tree, (0, 180, 120, 22), "杉木")
        self.tree7 = Check(self.page_tree, (130, 180, 120, 22), "梦见木")
        self.tree8 = Check(self.page_tree, (260, 180, 120, 22), "枫木")
        self.tree9 = Check(self.page_tree, (0, 216, 120, 40), "孔雀木\n御伽木")
        self.tree10 = Check(self.page_tree, (130, 225, 120, 22), "御伽木")
        self.tree11 = Check(self.page_tree, (260, 216, 120, 40), "业果木\n辉木")
        self.tree12 = Check(self.page_tree, (0, 270, 120, 22), "证悟木")
        self.tree13 = Check(self.page_tree, (130, 270, 120, 22), "刺葵木")
        self.tree14 = Check(self.page_tree, (260, 270, 120, 22), "悬铃木")
        self.tree15 = Check(self.page_tree, (0, 315, 120, 22), "椴木")
        self.tree16 = Check(self.page_tree, (130, 315, 120, 22), "白岑木")
        self.tree17 = Check(self.page_tree, (260, 315, 120, 22), "香柏木")
        self.tree18 = Check(self.page_tree, (0, 360, 120, 22), "炬木")


domain_dir = {
    "圣遗物":
        ["仲夏庭园", "铭记之谷", "孤云凌霄之处",
         "无妄引咎密宫", "华池岩岫", "芬德尼尔之顶",
         "山脊守望", "椛染之庭", "沉眠之庭",
         "岩中幽谷", "缘觉塔", "赤金的城墟",
         "熔铁的孤塞", "罪祸的终末",
         "临瀑之城", "虹灵的净土"],
    "天赋培养素材":
        ["忘却之峡", "太山府", "菫色之庭",
         "昏识塔", "苍白的遗荣", "蕴火的幽墟"],
    "武器突破素材":
        ["塞西莉亚苗圃", "震雷连山密宫", "砂流之庭",
         "有顶塔", "深潮的余响", "深古瞭望所"]}






class Pass:
    def __init__(self, stack):
        # 初始化窗口
        self.page_pass = Widget(stack)
        stack.addWidget(self.page_pass)
        # 添加控件
        self.label_pass = Label(self.page_pass, (0, 12, 180, 18), "设置页面：领取纪行")
        self.label_pass_tip = Label(self.page_pass, (90, 80, 220, 27), "领取纪行 暂无配置项目。")


class GenshinStack(Local, Run_way,Team, Disp, Trans, Fly, Daily, Pot, Mail, Tree, Pass):
    def __init__(self, widget, location):
        # 功能堆叠窗口
        self.stack = Stack(widget, location)
        Local.__init__(self, self.stack)
        Run_way.__init__(self, self.stack)
        Team.__init__(self, self.stack)
        Disp.__init__(self, self.stack)
        Trans.__init__(self, self.stack)
        Fly.__init__(self, self.stack)
        Daily.__init__(self, self.stack)
        Pot.__init__(self, self.stack)
        Mail.__init__(self, self.stack)
        Tree.__init__(self, self.stack)
        Pass.__init__(self, self.stack)