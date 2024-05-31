# -*- coding:gbk -*-
from ui.element.ui_part import Independent
from ui.element.control import *


class Local:
    def __init__(self, stack):
        # 初始化窗口
        self.page_local = Widget(stack)
        stack.addWidget(self.page_local)
        # 添加控件
        self.label_local = Label(self.page_local, (0, 12, 180, 18), "设置页面：尘白禁区 运行方式")
        Line(self.page_local, (0, 42, 395, 3))

        self.label_snow_overall = Label(self.page_local, (0, 50, 180, 27), "全局设置：")
        self.label_start = Label(self.page_local, (0, 90, 80, 27), "服务器")  # 启动路径 /
        self.combo_server = Combobox(self.page_local, (80, 90, 100, 32))
        self.combo_server.addItems(["官服", "B服"])
        self.label_start = Label(self.page_local, (0, 130, 80, 27), "启动路径")
        self.line_start = Lineedit(self.page_local, (0, 160, 385, 33))

        Line(self.page_local, (0, 202, 395, 3))

        self.label_team_tip = Label(self.page_local, (0, 210, 220, 27), "独立运行设置：")
        self.check_preload = Check(self.page_local, (0, 245, 140, 22), "自动预下载")
        self.check_update = Check(self.page_local, (205, 245, 140, 22), "自动更新")
        self.independent = Independent(self.page_local, (0, 285, 350, 70))
        self.label_tools = Label(self.page_local, (0, 365, 220, 27), "实用工具：")
        self.button_wiki = Button(self.page_local, (0, 400, 100, 30), "天启者图鉴")

        self.label_account = Label(self.page_local, (0, 433, 220, 27), "账号选择：")
        self.line_account = Lineedit(self.page_local, (0, 467, 200, 33))


class Fight:
    def __init__(self, stack):
        # 初始化窗口
        self.page_fight = Widget(stack)
        stack.addWidget(self.page_fight)
        # 添加控件
        self.label_fight = Label(self.page_fight, (0, 12, 220, 18), "设置页面：感知扫荡")

        self.check_share = Check(self.page_fight, (15, 50, 140, 22), "感知互赠")
        self.check_supply = Check(self.page_fight, (15, 80, 140, 22), "每日配给")
        self.check_reagent = Check(self.page_fight, (15, 110, 140, 22), "无限使用限时试剂")

        self.label_mat = Label(self.page_fight, (15, 195, 80, 18), "剩余感知")
        self.mat = Combobox(self.page_fight, (15, 225, 180, 40))
        self.mat.addItems(
            ["通用银", "角色经验素材", "武器经验素材",
             "武器突破素材", "角色神经素材", "后勤获取",
             "活动后勤获取", "活动武器获取",
             "活动关卡-幻现幻归"])

        self.label_logistics = Label(self.page_fight, (15, 275, 80, 18), "后勤选择")
        self.logistics = Combobox(self.page_fight, (15, 305, 160, 40))
        self.logistics.addItems(
            ["底比斯小队",
             "芬尼亚小队",
             "摩伊拉小队",
             "天岩户小队",
             "曙光小队",
             "新叶小队",
             "达摩小队",
             "凯夫曼小队"])
        self.logistics1 = Combobox(self.page_fight, (185, 305, 160, 40))
        self.logistics1.addItems(
            ["明夷小队",
             "秋津小队",
             "阿玛纳小队",
             "心园小队",
             "伊莱小队",
             "极光小队",
             "祖灵小队",
             "沙叶小队"])


class Daily:
    def __init__(self, stack):
        # 初始化窗口
        self.page_debris = Widget(stack)
        stack.addWidget(self.page_debris)
        # 添加控件
        self.label_debris = Label(self.page_debris, (0, 12, 180, 18), "设置页面：日常周常")

        self.check_character = Check(self.page_debris, (15, 50, 140, 22), "个人故事")
        self.check_supplement = Check(self.page_debris, (15, 80, 250, 22), "嵌片为0时,启用2个补嵌包")
        self.character1 = Combobox(self.page_debris, (15, 110, 120, 40))
        self.character2 = Combobox(self.page_debris, (145, 110, 120, 40))
        self.character3 = Combobox(self.page_debris, (15, 155, 120, 40))
        self.character4 = Combobox(self.page_debris, (145, 155, 120, 40))
        chara = ["未选择", "瞬刻", "羽蜕", "悖谬", "豹豹", "蓝闪", "魔术师", "藏锋", "溯影", "云篆", "辉夜",
                 "咎冠", "冬至", "狂猎", "雨燕", "缄默",
                 "小金鱼", "小太阳", "观测者", "黄金狮子", "养生专家",
                 "猫猫", "星期三", "姐姐大人", "双面", "旧日王牌",
                 "绷带小组", "不予显示", "四手"]
        self.character1.addItems(chara)
        self.character2.addItems(chara)
        self.character3.addItems(chara)
        self.character4.addItems(chara)

        self.check_imitate = Check(self.page_debris, (15, 210, 140, 22), "拟境扫荡")

        self.check_market = Check(self.page_debris, (15, 255, 220, 22), "通过商店购物一次完成每日")
        self.box_market1 = Combobox(self.page_debris, (15, 285, 160, 40))
        self.box_market2 = Combobox(self.page_debris, (180, 285, 160, 40))
        self.box_market1.addItems(["新手战斗记录", "初级职级认证", "芳烃塑料", "芳烃塑料×3"])
        self.box_market2.addItems(["新手战斗记录", "初级职级认证", "芳烃塑料", "芳烃塑料×3"])
        self.check_weapon = Check(self.page_debris, (15, 340, 220, 22), "通过武器升级一次完成每日")

        self.check_daily = Check(self.page_debris, (15, 375, 140, 22), "领取日常")
        self.check_daily2 = Check(self.page_debris, (15, 410, 140, 22), "领取凭证")
        self.check_daily3 = Check(self.page_debris, (15, 445, 180, 22), "领取活动每日-幻现幻归")


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
        self.label_roll = Label(self.page_roll, (0, 12, 180, 18), "设置页面：共鸣记录")
        self.button_arrange = Button(self.page_roll, (0, 45, 180, 30), "导出共鸣记录为Excel")
        self.button_open_roll = (
            TransPicButton(self.page_roll, (185, 45, 30, 30),
                           "assets/main_window/ui/directory.png", (25, 25)))
        self.label_roll_tip = Label(self.page_roll, (90, 100, 220, 27), "共鸣记录 暂无配置项目。")


class SnowStack(Local, Fight, Daily, Mail, Roll):
    def __init__(self, widget, location):
        # 功能堆叠窗口
        self.stack = Stack(widget, location)
        Local.__init__(self, self.stack)
        Fight.__init__(self, self.stack)
        Daily.__init__(self, self.stack)
        Mail.__init__(self, self.stack)
        Roll.__init__(self, self.stack)
