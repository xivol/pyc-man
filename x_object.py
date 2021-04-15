import pygame


def is_collided(self, target):
    return self.get_hit_box().colliderect(target.get_hit_box())


class XStaticObject(pygame.sprite.Sprite):
    __sprite_name__ = None

    def __init__(self, image, rect, position=None, *groups):
        super().__init__(*groups)
        self.rect = rect
        self.image = image

        if position:
            self.rect.center = position

    @classmethod
    def sprite_name(cls):
        return cls.__sprite_name__


    def get_hit_box(self):
        return self.rect

    def get_hit(self, colliders, collide_func=is_collided ):
        if self in colliders.sprites():
            colliders.remove(self)

            hit = pygame.sprite.spritecollideany(self, colliders, collide_func)
            colliders.add(self)
        else:
            hit = pygame.sprite.spritecollideany(self, colliders, collide_func)
        return hit


class XAnimatedObject(XStaticObject):
    __animations__ = None
    __default_state__ = None
    __manager_type__ = None

    def __init__(self, manager, position=None, *groups):
        self.animation = manager
        img = self.animation.current().image()
        rect = img.get_rect()
        super().__init__(img,rect,position, *groups)

    def update(self, timedelta, *params):
        self.animate(timedelta)

    def animate(self, timedelta):
        self.image = self.animation.current().image()
        self.animation.update(timedelta)
