import pygame


class XObject(pygame.sprite.Sprite):
    __sprite_name__ = None

    @classmethod
    def sprite_name(cls):
        return cls.__sprite_name__

    @staticmethod
    def collided(subject, target):
        return subject.get_hit_box().colliderect(target.get_hit_box())

    def get_hit_box(self):
        return self.rect

    def get_hit(self, colliders):
        if self in colliders.sprites():
            colliders.remove(self)
            hit = pygame.sprite.spritecollideany(self, colliders, XObject.collided)
            colliders.add(self)
        else:
            hit = pygame.sprite.spritecollideany(self, colliders, XObject.collided)
        return hit


class XStaticObject(XObject):
    def __init__(self, image, rect, position=None, *groups):
        super().__init__(*groups)
        self.rect = rect
        self.image = image

        if position:
            self.rect.center = position


class XAnimatedObject(XObject):
    __sprite_name__ = None
    __animations__ = None
    __default_state__ = None
    __manager_type__ = None

    def __init__(self, manager, position=None, *groups):
        super().__init__(*groups)
        self.animation = manager
        self.image = img = self.animation.current().image()
        self.rect = img.get_rect()
        if position:
            self.rect.center = position

    def update(self, timedelta, *params):
        self.animate(timedelta)

    def animate(self, timedelta):
        self.image = self.animation.current().image()
        self.animation.update(timedelta)
