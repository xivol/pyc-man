import pygame


class XUI(pygame.sprite.Sprite):
    def set_position(self, position):
        x, y = position
        self.rect = pygame.Rect(x, y, self.rect.width, self.rect.height)

    def update(self, timedelta):
        pass
