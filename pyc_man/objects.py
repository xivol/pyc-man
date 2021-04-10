import pygame
import x_object


class Wall(x_object.XObject):
    pass


class Gate(x_object.XObject):
    pass


class Bonus(x_object.XObject):
    def __init__(self, points, *params):
        super().__init__(*params)
        self.points = points


class Pellet(Bonus):
    __sprite_name__ = 'pellet'

    def __init__(self, *params):
        super().__init__(10, *params)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width//4, self.rect.height//4)
        hit_box.center = self.rect.center
        return hit_box


class Energizer(Bonus):
    __sprite_name__ = 'energizer'

    def __init__(self, *params):
        super().__init__(50, *params)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width//2, self.rect.height//2)
        hit_box.center = self.rect.center
        return hit_box


class Fruits(Bonus, x_object.SpawnableMixin):
    __points__ = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
    __sprite_name__ = 'fruit'
    __spawnpoint__ = 'fruit'

    def __init__(self, *params, **kwargs):
        i = kwargs.get('order', 0)
        super().__init__(self.__points__[i], *params)

    @classmethod
    def count(cls):
        return 8

    @classmethod
    def sprite_name(cls, i):
        return cls.__sprite_name__ + '-' + str(i+1)
