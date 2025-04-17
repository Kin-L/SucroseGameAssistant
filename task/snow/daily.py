from tools.environment import *
from ..default_task import Task


class Daily(Task):
    def __init__(self):
        super().__init__()

    def snow_daily(self):
        self.indicate("开始检查：日常周常")
        if self.task["个人故事"][0]:
            click_change((1690, 470), (1552, 468, 1626, 515))
            pos = wait_text("个人", (733, 812, 947, 891))
            click_change(pos, (733, 812, 947, 891))
            _u = 0
            for i in self.task["个人故事"][2:]:
                if i != "未选择":

                    if i == "缄默":
                        _r = "默"
                    elif i == "咎冠":
                        _r = "冠"
                    elif i == "悖谬":
                        _r = "谬"
                    elif i == "魔术师":
                        _r = "术师"
                    elif i == "驰掣":
                        _r = "驰"
                    else:
                        _r = i
                    _f = False
                    cl = False
                    for o in range(8):
                        pos = find_text(_r, (0, 731, 1417, 858))
                        if pos:
                            (_x, _y) = pos
                            _str = ocr((_x+267, 177,  _x+447, 233))[0]

                            if "0" in _str or "o" in _str or "O" in _str:
                                self.indicate(f"今日已完成：角色 {i}")
                                _f = True
                            elif "1" in _str or "i" in _str or "I" in _str:
                                pass
                            else:
                                cl = True
                            break
                        elif o == 7:
                            roll((1002, 581), 250)
                            wait(800)
                            _f = True
                            self.indicate(f"未识别到角色: {i}")
                        else:
                            roll((1002, 581), -25)
                            wait(800)
                    if _f:
                        continue
                    sc = scshot()
                    _str1 = ocr((1459, 27, 1540, 77), sc)[0]
                    _str2 = numfind(_str1.split("/")[0])
                    try:
                        _num = int(_str2)
                    except ValueError:
                        self.indicate(f"记忆嵌片数量识别异常")
                        _path = errorsc_save(sc)
                        logger.error(f":_str {_str1}")
                        logger.error(f"截图导出: {_path}")
                        return 0
                    if _num == 0 and self.task["个人故事"][1] and _u < 2:
                        _u += 1
                        click_change((1566, 51), (1547, 38, 1584, 69))
                        wait(500)
                        if ocr((1354, 717, 1552, 817))[0] == "确定":
                            if cl:
                                click_change((1221, 626), (934, 595, 990, 656))
                            click_change(pos, (1354, 717, 1552, 817))
                            wait_text("获得道具", (809, 40, 1113, 147))
                            click_change((1037, 951), (809, 40, 1113, 147))
                        else:
                            self.indicate(f"补嵌包不足")
                            break
                    elif _num > 2:
                        pass
                    else:
                        self.indicate(f"记忆嵌片不足: {_num}")
                        break
                    click_change((_x, 900), (858, 801, 1072, 875))
                    if cl:
                        click_change((1168, 718), (875, 685, 945, 749))
                    click_text("开始", (858, 801, 1072, 875))
                    wait_text("完成", (929, 965, 1041, 1028))
                    self.indicate(f"完成个人故事扫荡 {i}")
                    press_to_pic("esc", r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
            press_to_text("esc", "任务", (1458, 330, 1529, 379))
            wait(500)
        if self.task["拟境扫荡"]:
            click_change((1690, 470), (1552, 468, 1626, 515))
            pos = wait_text("特别", (157, 464, 425, 560))
            click_change(pos, (157, 464, 425, 560))
            x, y = wait_text("精神", (150, 770, 1779, 848))
            click_change((x, 462), (61, 998, 245, 1059))
            wait_text("斗", (1288, 180, 1451, 239))
            for _p in [(224, 253), (216, 394)]:
                click(_p)
                wait(800)
                for i in range(4):
                    sc = scshot()
                    if ("快速" in ocr((1351, 977, 1512, 1052), sc)[0] and
                            int(ocr((1791, 576, 1852, 611), sc)[0].replace(" ", "")[:-2]) > 0):
                        del sc
                        click_change((1415, 999), (1358, 964, 1548, 1071))
                        wait(500)
                        click_change((1375, 773), (1358, 964, 1548, 1071))
                        wait(500)
                        self.indicate("拟境扫荡一次")
                    else:
                        del sc
                        break
            if find_color("yellow", (188, 869, 195, 876))[1]:
                click_change((137, 914), (107, 883, 179, 948))
                click_change((1742, 1001), (1670, 971, 1830, 1022))
                wait_text("获得道具", (809, 40, 1113, 147))
                self.indicate("领取评测奖励")
                press_to_pic("esc", r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
            press_to_text("esc", "任务", (1458, 330, 1529, 379))
            wait(500)
        if self.task["商店购物"][0]:
            click_text("商店", (1756, 997, 1852, 1061))
            wait_pic(r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
            roll((1241, 380), -20)
            wait(500)
            for i in [self.task["商店购物"][1], self.task["商店购物"][2]]:
                _f = False
                if "×" in i:
                    i = i.split("×")[0]
                    _f = True
                pos = find_text(i, (323, 213, 1860, 1003))
                if pos:
                    click_change(pos, (1723, 981, 1840, 1044))
                    if _f:
                        click_change((1832, 853), (1545, 834, 1582, 874))
                    break
            click_to_pic((1782, 1014), r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
            self.indicate("商店购物一次")
            press_to_text("esc", "任务", (1458, 330, 1529, 379))
            wait(500)
        if self.task["武器升级"]:
            click_text("背包", (1599, 994, 1692, 1063))
            wait(500)
            # 排序
            click_change((73, 1025), (50, 1011, 111, 1056))
            wait(500)
            click_change((585, 327), (625, 303, 681, 349))
            click_change((585, 327), (625, 303, 681, 349))
            click_change((1316, 840), (1302, 798, 1435, 893))
            # 升级
            click_change((425, 191), (50, 1011, 111, 1056))
            click_change((985, 774), (50, 1011, 111, 1056))
            click_change((181, 300), (123, 263, 248, 332))
            pos = wait_text("升级", (1691, 981, 1818, 1053))
            click_change((1383, 717), (123, 263, 248, 332))
            click_change((119, 168), (1341, 675, 1431, 766))
            click_change(pos, (1691, 981, 1818, 1053))
            wait_text("升", (869, 323, 1051, 408))
            self.indicate("武器升级一次")
            press_to_text("esc", "任务", (1458, 330, 1529, 379))
            wait(500)
        if self.task["领取日常"]:
            click_text("任务", (1440, 311, 1555, 403))
            wait(500)
            pos = find_text("领取", (55, 973, 197, 1023))
            if pos:
                click_change(pos, (18, 952, 242, 1040))
                click_to_pic(pos, r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
                self.indicate("领取日常奖励")
                wait(500)
            click((101, 257))
            wait(800)
            pos = find_text("领取", (55, 973, 197, 1023))
            if pos:
                click_change(pos, (18, 952, 242, 1040))
                click_to_pic(pos, r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
                self.indicate("领取周常奖励")
            press_to_text("esc", "任务", (1458, 330, 1529, 379))
            wait(500)
        if self.task["领取凭证"] and find_color("yellow", (379, 557, 387, 566))[1]:
            click_change((311, 580), (283, 560, 366, 599))
            for _p in [(1272, 1025), (1512, 1027), (1052, 1029)]:
                click(_p)
                wait(300)
                pos = find_text("领取", (76, 1000, 220, 1045))
                if pos:
                    click_change(pos, (76, 1000, 220, 1045))
                    wait_text("获得道具", (809, 40, 1113, 147))
                    self.indicate("领取凭证奖励")
                    click_change(pos, (809, 40, 1113, 147))
            press_to_text("esc", "任务", (1458, 330, 1529, 379))
            wait(500)
        if self.task["活动每日"]:
            if ocr((1378, 420, 1460, 457))[0]:
                click_change((1499, 538), (1402, 463, 1499, 505))
                wait_pic(r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
                wait(300)
                pos = find_text("任务")
                cpos = (1081, 1025)  # 渊沉曙色
                if pos:
                    x, y = pos
                    click_change(pos, (x-10, y-10, x+10,  y+10))
                    pos = wait_text("领取", (0, 605, 578, 1080))

                else:
                    click(cpos)
                    wait(1000)
                    pos = find_text("领取", (0, 605, 578, 1080))
                    if pos:
                        pass
                    else:
                        self.indicate("未找到“任务”, 版本未适配")
                        press_to_text("esc", "任务", (1458, 330, 1529, 379))
                        wait(500)
                        self.indicate("检查完成：日常周常")
                        return True
                click_change(pos, (76, 1000, 220, 1045))
                wait_text("获得道具", (809, 40, 1113, 147))
                self.indicate("领取已完成的活动任务")
                click_change(pos, (809, 40, 1113, 147))
                press_to_text("esc", "任务", (1458, 330, 1529, 379))
                wait(500)
            else:
                self.indicate(f"本期活动已关闭")
        if self.task["信源断片"]:
            click_change((1629, 710), (1570, 675, 1689, 751))
            press_to_text("esc", "分析员", (1716, 156, 1811, 207))
            click_change((1629, 710), (1514, 1022, 1611, 1067))
            wait(500)
            click_change((1471, 765), (1383, 733, 1547, 798))
            wait(500)
            if ocr((1716, 156, 1811, 207))[0] == "分析员":
                self.indicate(f"暂无断片可收获")
            else:
                wait_text("芙", (852, 804, 1065, 875))
                click_change((960, 838), (852, 804, 1065, 875))
                self.indicate(f"收取到信源断片")
                wait(500)
            click_change((1652, 46), (1626, 27, 1685, 65))
            wait(500)
            wait_text("任务", (1458, 330, 1529, 379))

        self.indicate("检查完成：日常周常")
