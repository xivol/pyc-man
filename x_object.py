import pygame


class SpawnableMixin:
    __spawnpoint__ = None

    @classmethod
    def spawnpoint(cls):
        return cls.__spawnpoint__


class XObject(pygame.sprite.Sprite):
    __sprite_name__ = None

    @classmethod
    def sprite_name(cls):
        return cls.__sprite_name__

    @staticmethod
    def collided(subject, target):
        return subject.get_hit_box().colliderect(target.get_hit_box())

    def __init__(self, image, rect, position=None, *groups):
        super().__init__(*groups)
        self.rect = rect
        self.image = image

        if position:
            self.rect.center = position

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
