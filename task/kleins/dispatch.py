from tools.environment import *
from ..default_task import Task


class Dispatch(Task):
    def __init__(self):
        super().__init__()
    
    def kleins_dispatch(self):
        click((146, 720))
        wait(1500)
        click((1563, 141))
        wait(1000)
        _list = [[176, 209], [285, 317], [394, 427],
                 [503, 539], [612, 645], [722, 755]]
        _c = [[735, 223], [734, 337], [734, 444],
              [739, 549], [737, 660], [733, 769]]
        _dir = {"线下采购材料":
                ["食油", "黄油", "生抽", "食盐", "胡椒",
                 "酱料", "糖类", "芥末", "香料粉", "西红柿醋"],
                "携带资金": ["零元购", "1000格", "2000格", "3000格"],
                "采购方案": ["固定物品", "额外物品", "减少时间"]}
        for n in range(6):
            y1, y2 = _list[n]
            _p = _c[n]
            zoom = (1068, y1, 1228, y2)
            _text = ocr(zoom)[0]
            if (":" in _text) or ("：" in _text):
                self.indicate("线下采购" + str(n + 1) + ":进行中")
                continue
            elif _text == "采购完成":
                click(_p)
                wait(400)
                click((1708, 977))
                wait(1200)
                if self.task["再次采购"]:
                    click((1208, 845))
                    self.indicate("线下采购" + str(n + 1) + ":完成 再次采购")
                    wait(1500)
                    continue
                else:
                    click((878, 851))
                    self.indicate("线下采购" + str(n + 1) + ":完成 已领取")
                wait(1200)
            elif _text == "尚未安排采购":
                self.indicate("线下采购" + str(n + 1) + ":待派遣")
                click(_p)
                wait(400)
            else:
                self.indicate("error:线下采购" + str(n + 1) + " 识别异常")
                raise RuntimeError("线下采购" + str(n + 1) + " 识别异常")
            click((1562, 939))
            wait(800)
            _mat, _fund, _plan = self.task[f"采购{n}"]
            _path = "assets/kleins/picture/dispatch/zone"+str(_mat)+".png"
            _p, sim = find_pic(_path, (666, 420, 1860, 484))
            if sim == 0:
                drag((1128, 451), (-200, 0))
                wait(800)
                _p, sim = find_pic(_path, (666, 420, 1860, 484))
            click(_p)
            wait(500)
            _p = [(951, 667), (961, 749), (960, 838)][_fund]
            click(_p)
            wait(500)
            click((1571, 883))
            wait(1500)
            _p, sim = find_pic(f"assets/kleins/picture/dispatch/plan{_plan}.png", (194, 145, 454, 585))
            if sim >= 0.85:
                click(_p)
                wait(500)
                self.indicate("线下采购开始:\n  " +
                              _dir["线下采购材料"][_mat] +
                              "\n  "+_dir["携带资金"][_fund] +
                              "\n  "+_dir["采购方案"][_plan])
            else:
                self.indicate("采购方案未找到目标，已自动选择一号位。")
                self.indicate("线下采购开始:\n  " +
                              _dir["线下采购材料"][_mat] +
                              "\n  "+_dir["携带资金"][_fund])
                click((143, 151))
                wait(500)
            click((397, 1008))
            wait(1500)
        # 结束
        click((296, 75))
        wait(1000)
