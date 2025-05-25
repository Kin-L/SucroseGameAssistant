class QtLocation(tuple):
    def __new__(cls, x: int, y: int, w: int, h: int):
        return super().__new__(cls, (x, y, w, h))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def w(self):
        return self[2]

    @property
    def h(self):
        return self[3]

    @property
    def position(self):
        return self[0], self[1]

    @property
    def size(self):
        return self[2], self[3]


class SGAZone(tuple):
    def __new__(cls, x1: int, y1: int, x2: int, y2: int):
        return super().__new__(cls, (x1, y1, x2, y2))

    @property
    def x1(self):
        return self[0]

    @property
    def y1(self):
        return self[1]

    @property
    def x2(self):
        return self[2]

    @property
    def y2(self):
        return self[3]

    @property
    def position1(self):
        return self[0], self[1]

    @property
    def position2(self):
        return self[2], self[1]

    @property
    def position3(self):
        return self[2], self[3]

    @property
    def position4(self):
        return self[0], self[3]

    @property
    def size(self):
        return self[2] - self[0], self[3] - self[1]

    @property
    def center(self):
        return int((self[2] + self[0])/2), int((self[3] - self[1])/2)


class SGAPosition(tuple):
    def __new__(cls, x: int, y: int):
        return super().__new__(cls, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]


if __name__ == "__main__":
    pass
