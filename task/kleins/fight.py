from tools.environment import *
from ..default_task import Task


class Fight(Task):
    def __init__(self):
        super().__init__()
        
    def kleins_fight(self):
        text = ocr((1675, 397, 1802, 439))[0]
        if (":" in text) or ("：" in text):
            self.indicate("重游进行中，不能再次开启作战。")
            return False
        elif text == "完成重游":
            click((1739, 420))
            self.indicate("重游完成，领取重游奖励。")
            wait(2500)
            while 1:
                sc = scshot()
                if "向导等级" in ocr((827, 134, 1088, 262), sc)[0].replace(" ", ""):
                    self.indicate("等级提升！")
                    click((1282, 690))
                    sc = scshot()
                if "再次重游" in ocr((1703, 50, 1832, 97), sc)[0].replace(" ", ""):
                    wait(500)
                    del sc
                    if self.task["再次重游"]:
                        click((1744, 80))
                        wait(1800)
                        _t = ocr((979, 290, 1855, 1051), mode=1)
                        for i in _t:
                            if "开始重游" in i[0]:
                                click((1533, 546))
                                wait(1000)
                                click((1445, 819))
                                wait(1500)
                            elif "追忆" in i[0]:
                                click((1687, 602))
                                wait(1000)
                                click((1606, 892))
                                wait(1500)
                            else:
                                continue
                            if "取消" in ocr((710, 756, 801, 806))[0].replace(" ", ""):
                                self.indicate("能源不足。")
                                click((761, 781))
                                wait(1000)
                                click((288, 78))
                                wait(1500)
                                return False
                            else:
                                self.indicate("开始重复上次作战。")
                                click((288, 78))
                                wait(1500)
                                return False
                        self.indicate("error:不能识别的界面")
                        click((288, 78))
                        wait(1500)
                        return True
                    else:
                        click((971, 930))
                        wait(800)
                    break
                del sc
                wait(1000)
        else:
            self.indicate("作战空闲中。")
        click((1446, 359))
        wait(1500)
        click((737, 1028))
        wait(1500)
        num = self.task["作战关卡"]
        _p = [(519, 545), (885, 554), (1248, 534)][num]
        click(_p)
        wait(2000)
        click((786, 555))
        wait(1500)
        click((1077, 856))
        wait(1000)
        click((1525, 549))
        wait(500)
        click((1458, 816))
        wait(1500)
        if "取消" in ocr((710, 756, 801, 806))[0].replace(" ", ""):
            self.indicate("能源不足。")
            click((761, 781))
            wait(1000)
        else:
            self.indicate("开始作战：获取 "+["格", "风物志", "节"][num])
        click((288, 78))
        wait(1500)
        return False
