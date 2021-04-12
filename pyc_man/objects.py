import pygame
import x_object
from x_animation import *


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
        hit_box = pygame.Rect(0, 0, self.rect.width // 3, self.rect.height // 3)
        hit_box.center = self.rect.center
        return hit_box


class Energizer(Bonus):
    __sprite_name__ = 'energizer'

    def __init__(self, *params):
        super().__init__(50, *params)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box


class Fruits(Bonus, x_object.SpawnableMixin):
    __points__ = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
    __sprite_name__ = 'fruit'

    @classmethod
    def sprite_name(cls, i):
        return cls.__sprite_name__ + '-' + str(i + 1)

    @classmethod
    def count(cls):
        return 8

    __spawnpoint__ = 'fruit'
    __animations__ = {"normal": StaticAnimation, "blinking": BlinkingAnimation}
    __default_state__ = "blinking"

    def __sprite_factory__(self):
        from x_sprite_factory import XSpriteFactory
        sf = XSpriteFactory()

        for i, anim_name in enumerate(XSpriteFactory.anim_sprite_names(self.__sprite_name__, self.__animations__)):
            sf.add(anim_name,
                   gid=-i-1, width=self.rect.width, height=self.rect.height,
                   frames=[self.image], durations=[100])
        return sf

    def __init__(self, *params, **kwargs):
        i = kwargs.get('order', 0)
        super().__init__(self.__points__[i], *params)
        self.animator = AnimationManager(self.__sprite_name__,
                                         self.__sprite_factory__(),
                                         self.__animations__,
                                         self.__default_state__)

    def update(self, timedelta):
        self.image = self.animator.current().image()
        self.animator.update(timedelta)

    def get_hit_box(self):
        hit_box = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        hit_box.center = self.rect.center
        return hit_box


