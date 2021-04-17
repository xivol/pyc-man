import pygame

import x_ui
from x_input import Direction


class UIText(x_ui.XUI):
    def __init__(self, text, font, color, align, *groups):
        super().__init__(*groups)
        self.text = text
        self.align = align
        self.color = color
        self.font = font
        self.__render__()

    def __render__(self):
        self.image = self.font.render(self.text, align=self.align, color=self.color)
        self.rect = self.image.get_rect()


class UIScoreCounter(UIText):
    def __init__(self, format_string, value, font, color=None, align='left',  *groups):
        self.value = value
        super().__init__(format_string, font, color, align, *groups)

    def set_value(self, new_value):
        if self.value != new_value:
            self.value = new_value
            self.__render__()

    def __render__(self):
        self.image = self.font.render(self.text.format(self.value), align= self.align, color=self.color)
        self.rect = self.image.get_rect()


class UICounter(x_ui.XUI):
    def __init__(self, count_images, start_value=0, min_value=None, max_value=None, direction=Direction.LEFT, *groups):
        super().__init__(*groups)
        self.images = count_images if isinstance(count_images, list) else [count_images]
        self.direction = direction
        self.max_value = max_value
        self.min_value = 0 if not min_value else min_value

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

            for i in range(self.min_value, self.value):
                img.blit(self.get_count_image(i), (x_start + i * w, 0))
            self.image = img

            if self.rect is not None:
                self.rect = pygame.Rect(self.rect.topleft, img.get_size())
            else:
                self.rect = pygame.Rect((0,0), img.get_size())

    def get_count_image(self, count):
        return self.images[count % len(self.images)]


class UILevelsCounter(UICounter):
    def set_value(self, new_value):
        if new_value > self.max_value:
            self.min_value = self.max_value - new_value
        super().set_value(new_value)
