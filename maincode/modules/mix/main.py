from ..main import ModuleClass
from .widget import MixPage
from maincode.modules.template import SubConfigTemplate
from typing import List
from maincode.main.subconfig import sc
from maincode.main.info import info


class MixConfig(SubConfigTemplate):
    ModuleKey: int = 0
    ConfigKeyList: List[str] = [""] * 8


def taskstart(self):
    self.mixpara = dict(self.para)
    self.mixpara["Accomplish"] = [False] * 8
    self.send(1)
    for num, (ck_, ac) in enumerate(zip(self.para["ConfigKeyList"], self.mixpara["Accomplish"])):
        if ck_ and not ac:
            _, _, mk, n = sc.FindItem(ck_)
            if not mk:
                self.send(f"连续任务 {num + 1} 无效")
                self.send(1)
                continue
            _dict = sc.Read(n)
            if ModuleClass.CheckConfig(_dict):
                self.__class__.substart = ModuleClass.Tasks[ModuleClass.FindItem(mk)[-1]]
                self.para = _dict
                self.para["OtherConfig"] = self.mixpara["OtherConfig"]
                self.para["SoftClose"] = True
                self.send(f"连续任务 {num + 1} 开始执行")
                self.substart()
                self.mixpara["Accomplish"][num] = True
                self.errornum = 0
                self.send(f"连续任务 {num + 1} 完成")
                self.send(1)
                self.send(f"等待5秒...")
                self.ctler.wait(5)
            else:
                self.send(f"连续任务 {num + 1} 配置读取异常")
                self.send(1)
                info.TaskError = True
                continue
        else:
            if ac:
                self.send(f"连续任务 {num + 1} 本轮已完成，跳过")
            else:
                self.send(f"连续任务 {num + 1} 未选择")
            self.send(1)
    self.para = self.mixpara


class MixClass(ModuleClass):
    def __init__(self):
        self.ModuleKey = 0
        self.ModuleNameCH = "连续任务"
        self.ModuleNameEN = "mix"
        self.IconPath = 'resources/main/SGA/default.png'
        self.Config = MixConfig
        self.Widget = MixPage()
        self.Task = taskstart
        super().__init__()
