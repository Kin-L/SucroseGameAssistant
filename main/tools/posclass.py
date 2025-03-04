from main.mainenvironment import sme


class Coordinate:
    # space : "AUTHOR" 1920*1080取点
    #         "WINDOW" 于本地游戏窗口的相对坐标,以窗口左上角为(0, 0)
    #         "SCREEN" 本地桌面
    # value : space 状态下的值
    # type  : value 是 点坐标(POINT) 还是 范围坐标(ZONE)
    # local : "SCREEN" 状态的值
    def __init__(self, coordinate, space=sme.space, vector=False):
        if isinstance(coordinate, Coordinate):
            self.value = coordinate.value
            self.space = coordinate.space
            self.type = coordinate.type
            self.local = coordinate.local
        else:
            if isinstance(coordinate, tuple):
                self.value = coordinate
            elif isinstance(coordinate, list):
                self.value = tuple(coordinate)
            else:
                raise ValueError("无效赋值类型")
            self.space = space
            if len(coordinate) == 2:
                if vector:
                    self.type = "VECTOR"
                else:
                    self.type = "POINT"
            elif len(coordinate) == 4:
                self.type = "ZONE"
            else:
                raise ValueError("无效赋值类型")
            self.local = self._tolocal()

    def _tolocal(self):
        if self.space == "AUTHOR":
            if self.type == "POINT":
                return np.add(np.rint(np.multiply(self.value, sme.zoom)), sme.position)
            elif self.type == "ZONE":
                return np.add(np.rint(np.multiply(self.value, sme.zoom)), sme.position + sme.position)
            else:
                return np.rint(np.multiply(self.value, sme.zoom))
        elif self.space == "SCREEN":
            return self.value
        elif self.space == "WINDOW":
            if self.type == "POINT":
                return np.add(self.value, sme.position)
            elif self.type == "ZONE":
                return np.add(sme.position, sme.position) + self.value
            else:
                return self.value

    def __repr__(self):
        return self.local


if __name__ == '__main__':
    import numpy as np
    cod = np.array([1, 2])
    c = np.array(cod)
    print(c)
    cod = Coordinate([1, 2])
    c = Coordinate(cod)
    print(c)
    print(isinstance(cod, Coordinate))
    print(type([1, 2]))
    print(type((1, 2)))
    print(type(np.array((1, 2))))
    print(list((1, 2)))
    print(tuple([1, 2]))