import pygame

import x_ui
from x_input import Direction


class UIScoreCounter(x_ui.XUI):
    def __init__(self, font, format_string, value, align, *groups):
        super().__init__(*groups)
        self.format_string = format_string
        self.font = font
        self.align = align
        self.value = None
        self.set_value(value)

    def set_value(self, new_value):
        if self.value != new_value:
            self.value = new_value
            self.image = self.font.render(self.format_string.format(self.value), align= self.align)
            self.rect = self.image.get_rect()


class UICounter(x_ui.XUI):
    def __init__(self, count_images, start_value=0, max_value=None, direction=Direction.LEFT, *groups):
        super().__init__(*groups)
        self.images = count_images if isinstance(count_images, list) else [count_images]
        self.direction = direction
        self.max_value = max_value

        self.value = None
        self.rect = None
        self.set_value(start_value)

    def set_value(self, new_value):
        if self.value != new_value:
            self.value = new_value
            w,h = self.images[0].get_size()

            img_w = w*self.value if not self.max_value else w*self.max_value

            img = pygame.Surface((img_w , h))

            if self.direction == Direction.RIGHT:
                x_start = img_w - w
                w = -w
            else:
                x_start = 0

            for i in range(self.value):
                img.blit(self.images[i % len(self.images)], (x_start + i * w, 0))
            self.image = img

            if self.rect is not None:
                self.rect = pygame.Rect(self.rect.topleft, img.get_size())
            else:
                self.rect = pygame.Rect((0,0), img.get_size())

class UILivesCounter(x_ui.XUI):
    pass


class UILevelsCounter(x_ui.XUI):
    pass