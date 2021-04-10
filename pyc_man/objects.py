import x_object


class Wall(x_object.XObject):
    pass


class Bonus(x_object.XObject):
    __sprite_name__ = None

    def __init__(self, points, *params):
        super().__init__(*params)
        self.points = points

    @classmethod
    def sprite_name(cls):
        return cls.__sprite_name__


class Pellet(Bonus):
    __sprite_name__ = 'pellet'

    def __init__(self, *params):
        super().__init__(10, *params)


class Energizer(Bonus):
    __sprite_name__ = 'energizer'

    def __init__(self, *params):
        super().__init__(50, *params)


class Fruits(Bonus):
    __points__ = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
    __sprite_name__ = 'fruit'

    def __init__(self, *params, **kwargs):
        i = kwargs.get('order', 0)
        super().__init__(self.__points__[i], *params)

    @classmethod
    def count(cls):
        return 8

    @classmethod
    def sprite_name(cls, i):
        return cls.__sprite_name__ + '-' + str(i+1)
