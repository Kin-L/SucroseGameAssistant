import json
from maincode.main.info import info
from maincode.tools.controls import (Combobox, SetStackPage, Check,
                                     ModuleStackPage, Widget, Line,
                                     Picture, TaskPanel, Label, tips,
                                     SLineEdit, PicButton, SetButton, TipsButton)
from typing import Optional
from os import path, startfile, getcwd
from PyQt5.QtWidgets import QFileDialog
_path = "resources/main/button/fold.png"


class SnowPage(ModuleStackPage):
    def __init__(self):
        super().__init__()
        self.wdlist: Optional[SnowList] = None
        self.page00: Optional[SnowPage00Set] = None
        self.page01: Optional[SnowPage01Set] = None
        self.page02: Optional[SnowPage02Set] = None
        self.page03: Optional[SnowPage03Set] = None
        self.page04: Optional[SnowPage04Set] = None
        self.picbt: Optional[Picture] = None
        self.pbset00 = None

    def LoadWidget(self):
        self.wdlist = SnowList()
        self.srlist.setWidget(self.wdlist)
        self.page00 = SnowPage00Set()
        self.page01 = SnowPage01Set()
        self.page02 = SnowPage02Set()
        self.page03 = SnowPage03Set()
        self.page04 = SnowPage04Set()
        self.sksetting.addWidget(self.page00)
        self.sksetting.addWidget(self.page01)
        self.sksetting.addWidget(self.page02)
        self.sksetting.addWidget(self.page03)
        self.sksetting.addWidget(self.page04)
        Line(self, (215, 5, 3, 530), False)
        self.pbset00 = SetButton(self, (180, 10, 25, 25), (25, 25))
        self.pbset00.clicked.connect(lambda: self.sksetting.setCurrentIndex(0))
        self.wdlist.pbset01.clicked.connect(lambda: self.sksetting.setCurrentIndex(1))
        self.wdlist.pbset02.clicked.connect(lambda: self.sksetting.setCurrentIndex(2))
        self.wdlist.pbset03.clicked.connect(lambda: self.sksetting.setCurrentIndex(3))
        self.wdlist.pbset04.clicked.connect(lambda: self.sksetting.setCurrentIndex(4))
        self.page01.btsnowlist.clicked.connect(lambda: startfile(f"{getcwd()}/resources/snow/list.json"))
        self.page02.btsnowlist.clicked.connect(lambda: startfile(f"{getcwd()}/resources/snow/list.json"))
        self.page04.btopenroll.clicked.connect(lambda: startfile(f"{getcwd()}/personal/snow/roll"))
        self.page00.btselect.clicked.connect(self.SelectPath)

    def SelectPath(self):
        self.page00.lepath.setText(QFileDialog.getOpenFileName(self, "选择启动路径")[0])

    def SetWidget(self, config: dict):
        self.page00.ckpreload.setChecked(config["PreLoad"])
        self.page00.ckupdate.setChecked(config["Update"])
        self.page00.leaccount.setText(config["AccountChoose"])
        _snow = info.OtherConfig["Snow"]
        self.page00.lepath.setText(_snow["Path"])
        self.page00.cbserver.setCurrentIndex(_snow["Server"])

        self.wdlist.ckitem01.setChecked(config["Energy"])
        self.wdlist.ckitem02.setChecked(config["DailyTask"])
        self.wdlist.ckitem03.setChecked(config["Other"])
        self.wdlist.ckitem04.setChecked(config["GachaRecog"])

        self.page01.ckmail.setChecked(config["Email"])
        self.page01.ckshare.setChecked(config["EnergyExchange"])
        self.page01.cksupply.setChecked(config["DailyEnergyPack"])
        self.page01.ckreagent.setChecked(config["EnergyDrug"])
        self.page01.cbmat.setCurrentIndex(config["LevelsChoose"])
        self.page01.comlogistics.setText(config["CommonLogistics"])
        self.page01.actlogistics.setText(config["ActivityLogistics"])

        self.page02.ckcharacter.setChecked(config["StoryEnable"])
        self.page02.cksupplement.setChecked(config["StoryUsePackage"])
        _list = config["StoryList"]
        self.page02.character1.setText(_list[0])
        self.page02.character2.setText(_list[1])
        self.page02.character3.setText(_list[2])
        self.page02.character4.setText(_list[3])
        self.page02.ckmarket.setChecked(config["ShopEnable"])
        _list = config["ShopList"]
        self.page02.cbmarket1.setText(_list[0])
        self.page02.cbmarket2.setText(_list[1])
        self.page02.ckweapon.setChecked(config["WeaponUp"])
        self.page02.ckdaily.setChecked(config["DailyTaskReceive"])
        self.page02.ckproof.setChecked(config["ProofReceive"])

        self.page03.ckimitate.setChecked(config["Simulation"])
        self.page03.ckactdaily.setChecked(config["ActivityDaily"])
        self.page03.ckinfofreg.setChecked(config["InfoFragment"])

        _list = config["GachaList"]
        self.page04.ckroll0.setChecked(_list[0])
        self.page04.ckroll1.setChecked(_list[1])
        self.page04.ckroll2.setChecked(_list[2])
        self.page04.ckroll3.setChecked(_list[3])
        self.page04.ckroll4.setChecked(_list[4])
        self.page04.ckroll5.setChecked(_list[5])
        self.page04.ckroll6.setChecked(_list[6])
        self.page04.ckopensheet.setChecked(config["GachaOpenSheet"])
        
        self.page00.taskpanel.ckkillsga.setChecked(config["SGAClose"])
        self.page00.taskpanel.ckmute.setChecked(config["Mute"])
        self.page00.taskpanel.ckkillprog.setChecked(config["SoftClose"])
        self.page00.taskpanel.cbafter.setCurrentIndex(config["Finished"])

    def CollectConfig(self) -> dict:
        _dict = dict()

        _dict["PreLoad"] = self.page00.ckpreload.isChecked()
        _dict["Update"] = self.page00.ckupdate.isChecked()
        _dict["AccountChoose"] = self.page00.leaccount.text()
        _otherdict = dict()
        _otherdict["Path"] = self.page00.lepath.text()
        _otherdict["Server"] = self.page00.cbserver.currentIndex()
        _dict["OtherConfig"] = {"Snow": _otherdict}

        _dict["Energy"] = self.wdlist.ckitem01.isChecked()
        _dict["DailyTask"] = self.wdlist.ckitem02.isChecked()
        _dict["Other"] = self.wdlist.ckitem03.isChecked()
        _dict["GachaRecog"] = self.wdlist.ckitem04.isChecked()

        _dict["Email"] = self.page01.ckmail.isChecked()
        _dict["EnergyExchange"] = self.page01.ckshare.isChecked()
        _dict["DailyEnergyPack"] = self.page01.cksupply.isChecked()
        _dict["EnergyDrug"] = self.page01.ckreagent.isChecked()
        _dict["LevelsChoose"] = self.page01.cbmat.currentIndex()
        _dict["CommonLogistics"] = self.page01.comlogistics.text()
        _dict["ActivityLogistics"] = self.page01.actlogistics.text()

        _dict["StoryEnable"] = self.page02.ckcharacter.isChecked()
        _dict["StoryUsePackage"] = self.page02.cksupplement.isChecked()
        _dict["StoryList"] = (
            self.page02.character1.text(),
            self.page02.character2.text(),
            self.page02.character3.text(),
            self.page02.character4.text())
        _dict["ShopEnable"] = self.page02.ckmarket.isChecked()
        _dict["ShopList"] = (self.page02.cbmarket1.text(), self.page02.cbmarket2.text())
        _dict["WeaponUp"] = self.page02.ckweapon.isChecked()
        _dict["DailyTaskReceive"] = self.page02.ckdaily.isChecked()
        _dict["ProofReceive"] = self.page02.ckproof.isChecked()

        _dict["Simulation"] = self.page03.ckimitate.isChecked()
        _dict["ActivityDaily"] = self.page03.ckactdaily.isChecked()
        _dict["InfoFragment"] = self.page03.ckinfofreg.isChecked()

        _dict["GachaList"] = (self.page04.ckroll0.isChecked(),
                              self.page04.ckroll1.isChecked(),
                              self.page04.ckroll2.isChecked(),
                              self.page04.ckroll3.isChecked(),
                              self.page04.ckroll4.isChecked(),
                              self.page04.ckroll5.isChecked(),
                              self.page04.ckroll6.isChecked())
        _dict["GachaOpenSheet"] = self.page04.ckopensheet.isChecked()

        _dict["Mute"] = self.page00.taskpanel.ckkillsga.isChecked()
        _dict["SoftClose"] = self.page00.taskpanel.ckmute.isChecked()
        _dict["Finished"] = self.page00.taskpanel.ckkillprog.isChecked()
        _dict["SGAClose"] = self.page00.taskpanel.cbafter.currentIndex()
        return _dict


class SnowList(Widget):
    def __init__(self):
        super().__init__()
        self.ckitem01 = Check(self, (0,   5, 120, 22), "感知扫荡")
        self.ckitem02 = Check(self, (0,  50, 120, 22), "日常任务")
        self.ckitem03 = Check(self, (0,  95, 120, 22), "其他任务")
        self.ckitem04 = Check(self, (0, 140, 120, 22), "共鸣记录")

        self.pbset01 = SetButton(self, (175,   5, 25, 25), (25, 25))
        self.pbset02 = SetButton(self, (175,  50, 25, 25), (25, 25))
        self.pbset03 = SetButton(self, (175,  95, 25, 25), (25, 25))
        self.pbset04 = SetButton(self, (175, 140, 25, 25), (25, 25))


class SnowPage00Set(SetStackPage):
    def __init__(self):
        super().__init__("设置页面：运行方式")
        self.lbsnowoverall = Label(self, (0, 55, 180, 27), "全局设置：")
        self.lbserver = Label(self, (0, 95, 80, 27), "服务器:")
        self.cbserver = Combobox(self, (80, 95, 100, 32))
        self.cbserver.addItems(["官服", "B服", "国际服", "模拟器"])
        tips(self.cbserver, '国际服需要提前手动开启加速器，模拟器只支持官服')

        self.lbpath = Label(self, (0, 135, 80, 27), "启动路径:")
        self.lepath = SLineEdit(self, (80, 135, 275, 33))
        tips(self.lepath, '官/B服填写启动器绝对路径，国际服填写游戏主目录‘SNOWBREAK’,模拟器填模拟器路径')
        self.btselect = PicButton(self, (360, 135, 35, 33), _path, (30, 30))
        Line(self, (0, 172, 395, 3))

        self.lbpartset = Label(self, (0, 175, 220, 27), "局部设置：")
        self.ckpreload = Check(self, (0, 215, 140, 22), "自动预下载")
        self.ckupdate = Check(self, (205, 215, 140, 22), "自动更新")
        self.lbaccount = Label(self, (0, 255, 120, 27), "账号选择：")
        self.leaccount = SLineEdit(self, (80, 255, 200, 33))
        if not path.exists("resources/snow/license.txt"):
            self.lbaccount.hide()
            self.leaccount.hide()
        Line(self, (0, 292, 395, 3))
        self.taskpanel = TaskPanel(self, 295)


class SnowPage01Set(SetStackPage):
    def __init__(self):
        super().__init__("设置页面：感知扫荡")
        self.ckmail = Check(self, (15, 55, 140, 22), "领取邮件")
        self.ckshare = Check(self, (15, 95, 140, 22), "感知互赠")
        self.cksupply = Check(self, (15, 135, 140, 22), "每日配给")
        self.ckreagent = Check(self, (15, 175, 140, 22), "无限使用限时试剂")

        self.lbmat = Label(self, (15, 220, 80, 18), "剩余感知:")
        self.cbmat = Combobox(self, (100, 210, 180, 40))
        self.cbmat.setMaxVisibleItems(5)
        self.cbmat.addItems(
            ["通用银", "角色经验素材", "武器经验素材",
             "武器突破素材", "角色神经素材", "后勤获取",
             "活动后勤获取", "活动武器获取",
             "活动材料关卡"])

        self.lblogistics = Label(self, (15, 265, 80, 18), "后勤选择:")
        self.comlogistics = Combobox(self, (15, 300, 160, 40))
        self.comlogistics.setMaxVisibleItems(5)
        self.comlogistics.addItems(
            ["底比斯小队",
             "芬尼亚小队",
             "摩伊拉小队",
             "天岩户小队",
             "曙光小队",
             "新叶小队",
             "达摩小队",
             "凯夫曼小队"])
        self.actlogistics = Combobox(self, (185, 300, 160, 40))
        self.actlogistics.setMaxVisibleItems(8)
        with open("resources/snow/list.json", 'r', encoding='utf-8') as g:
            _dir = json.load(g)
        self.actlogistics.addItems(
            _dir["活动后勤"])

        self.btsnowlist = PicButton(self, (100, 260, 30, 30), _path, (25, 25))
        tips(self.btsnowlist, "活动后勤自定义添加")


class SnowPage02Set(SetStackPage):
    def __init__(self):
        super().__init__("设置页面：日常任务")
        self.ckcharacter = Check(self, (15, 55, 140, 22), "个人故事")
        self.btsnowlist = PicButton(self, (110, 55, 30, 30), _path, (25, 25))
        tips(self.btsnowlist, "角色选择自定义添加")
        self.cksupplement = Check(self, (15, 85, 250, 22), "嵌片为0时,启用2个补嵌包")
        self.character1 = Combobox(self, (15,  120, 120, 40))
        self.character2 = Combobox(self, (145, 120, 120, 40))
        self.character3 = Combobox(self, (15,  165, 120, 40))
        self.character4 = Combobox(self, (145, 165, 120, 40))
        self.character1.setMaxVisibleItems(8)
        self.character2.setMaxVisibleItems(8)
        self.character3.setMaxVisibleItems(8)
        self.character4.setMaxVisibleItems(8)
        with open(r"resources/snow/list.json", 'r', encoding='utf-8') as g:
            _dir = json.load(g)

        chara = ["未选择"] + _dir["个人故事"]
        self.character1.addItems(chara)
        self.character2.addItems(chara)
        self.character3.addItems(chara)
        self.character4.addItems(chara)

        self.ckmarket = Check(self, (15, 220, 220, 22), "通过商店购物一次完成每日")
        self.shoptips = TipsButton(self, (200, 260), "常规物资商店并不划算，建议在通用银溢出后再用来置换资源")
        self.cbmarket1 = Combobox(self, (15,  250, 160, 40))
        self.cbmarket2 = Combobox(self, (180, 250, 160, 40))
        _list = ["光纤轴突", "光纤轴突×5",
                 "合成颗粒", "合成颗粒×5",
                 "芳烃塑料", "芳烃塑料×3",
                 "单极纤维", "单极纤维×2",
                 "通用强化套件", "通用强化套件×5",
                 "新手战斗记录", "新手战斗记录×5",
                 "初级职级认证", "初级职级认证×5",
                 "优选强化套件", "优选强化套件×3",
                 "普通战斗记录", "普通战斗记录×3",
                 "优秀战斗记录", "优秀战斗记录×2",
                 "高级职级认证", "高级职级认证×2"
                 ]
        self.cbmarket1.addItems(_list)
        self.cbmarket1.setMaxVisibleItems(8)
        self.cbmarket2.addItems(_list)
        self.cbmarket2.setMaxVisibleItems(8)
        self.ckweapon = Check(self, (15, 305, 220, 22), "通过武器升级一次完成每日")

        self.ckdaily = Check(self, (15, 340, 140, 22), "领取日常")
        self.ckproof = Check(self, (15, 375, 140, 22), "领取凭证")


class SnowPage03Set(SetStackPage):
    def __init__(self):
        super().__init__("设置页面：其他任务")
        self.ckimitate = Check(self, (15, 60, 140, 22), "拟境扫荡")
        self.ckactdaily = Check(self, (15, 100, 180, 22), "领取活动每日")
        self.ckinfofreg = Check(self, (15, 140, 180, 22), "收取信源断片")


class SnowPage04Set(SetStackPage):
    def __init__(self):
        super().__init__("设置页面：共鸣记录")
        self.btopenroll = PicButton(self, (150, 300, 30, 30), _path, (25, 25))
        self.ckroll0 = Check(self, (0, 55, 150, 30), "特选角色共鸣")
        self.ckroll1 = Check(self, (0, 90, 150, 30), "特选武器共鸣")
        self.ckroll2 = Check(self, (0, 125, 150, 30), "限定角色共鸣")
        self.ckroll3 = Check(self, (0, 160, 150, 30), "限定武器共鸣")
        self.ckroll4 = Check(self, (0, 195, 150, 30), "常守之誓")
        self.ckroll5 = Check(self, (0, 230, 150, 30), "中庭炉心")
        self.ckroll6 = Check(self, (0, 265, 150, 30), "新手池")

        self.ckopensheet = Check(self, (0, 300, 150, 30), "完成后打开表格")
