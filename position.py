class Position(tuple):
    def __new__(cls, x, y):
        return super().__new__(cls, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def radius(self):
        return 2

    def __add__(self, position):
        new_x = self.x + position.x
        new_y = self.y + position.y
        return self.__new__(self.__class__, new_x, new_y)
