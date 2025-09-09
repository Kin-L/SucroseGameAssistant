from maincode.modules.main import ModuleClass
from maincode.modules.mix.widget import MixPage
from maincode.modules.template import SubConfigTemplate
from typing import List
from maincode.config.subconfig import subconfig
from maincode.config.info import info
from maincode.tools.core.constant import spr

# 常量定义
TASK_COUNT = 8
WAIT_TIME = 5


class MixConfig(SubConfigTemplate):
    ModuleKey: int = 0
    ConfigKeyList: List[str] = ["" for _ in range(TASK_COUNT)]


def taskstart(self):
    self.mixpara = dict(self.para)
    self.mixpara["Accomplish"] = [False] * TASK_COUNT
    self.send(1)

    config_key_list = self.para.get("ConfigKeyList", [])
    accomplish_list = self.mixpara["Accomplish"]

    if len(config_key_list) != TASK_COUNT:
        self.send("配置项数量不匹配")
        return

    for num, (ck_, ac) in enumerate(zip(config_key_list, accomplish_list)):
        if ck_ != "" and not ac:
            try:
                _, na, mk, n = subconfig.FindItem(ck_)
                if not mk:
                    self.send(f"连续任务 {num + 1} 无效")
                    self.send(1)
                    continue
                _dict = subconfig.Read(n)
                if ModuleClass.CheckConfig(_dict):
                    # 避免直接修改类属性
                    substart_func = ModuleClass.Tasks[ModuleClass.FindItem(mk)[-1]]
                    self.para = _dict
                    self.para["OtherConfig"] = self.mixpara.get("OtherConfig", {})
                    self.para["SoftClose"] = True
                    if num:
                        self.send(f"等待{WAIT_TIME}秒...")
                        self.ctler.wait(WAIT_TIME)
                    self.send(f"连续任务 {num + 1} 开始执行")
                    self.send(f"       {ck_}{na}", False)
                    substart_func(self)  # 调用实例方法
                    self.mixpara["Accomplish"][num] = True
                    self.errornum = 0
                    self.send(f"连续任务 {num + 1} 完成")
                    self.send(1)
                else:
                    self.send(f"连续任务 {num + 1} 配置读取异常")
                    self.send(f"       {ck_}{na}", False)
                    self.send(1)
                    info.TaskError = True
                    continue
            except Exception as e:
                self.send(f"执行连续任务 {num + 1} 发生异常: {str(e)}")
                self.send(1)
                info.TaskError = True
        else:
            if ac:
                self.send(f"连续任务 {num + 1} 本轮已完成，跳过")
            else:
                self.send(f"连续任务 {num + 1} 未选择")
            self.send(1)
    self.para = self.mixpara


class MixClass(ModuleClass):
    ModuleNameCH = "连续任务"

    def __init__(self):
        self.ModuleKey = 0
        self.ModuleNameEN = "mix"
        self.IconPath = spr.SGAdefaultPic
        self.Config = MixConfig
        self.Widget = MixPage()
        self.Task = taskstart
        self.LoadModule = True
        super().__init__()
