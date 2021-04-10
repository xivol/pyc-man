import pygame
from pygame.rect import Rect


class XObject(pygame.sprite.Sprite):
    @staticmethod
    def collided(subject, target):
        if subject.get_hit_box().colliderect(target.get_hit_box()):
            print(subject.get_hit_box(), target.get_hit_box())
        return subject.get_hit_box().colliderect(target.get_hit_box())

    def __init__(self, image, rect, position=None, *groups):
        super().__init__(*groups)
        self.rect = rect
        self.image = image

        if position:
            self.rect.center = position

    def get_hit_box(self):
        return self.rect
