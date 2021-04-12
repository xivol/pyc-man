import pygame
import pytmx


class XBMPFont:

    def __init__(self, filename):
        tmx_data = pytmx.load_pygame(filename, load_all=True)
        self.__raw_data__ = tmx_data
        self.__ABC__ = {}
        for gid, props in tmx_data.tile_properties.items():
            self.__ABC__[props['type']] = tmx_data.get_tile_image_by_gid(gid)

    def render(self, string, **params):
        def normal(x):
            return x
        strings = string.split('\n')
        tw = self.__raw_data__.tilewidth
        th = self.__raw_data__.tileheight
        text_surface = pygame.Surface((tw * max(map(len, strings)), th * len(strings)))

        if 'align' in params and params['align'] == 'right':
            x_start = text_surface.get_size()[0]-tw
            tw = -tw
            transform = reversed
        else:
            x_start = 0
            transform = normal

        y = 0
        for string in strings:
            images = map(lambda c: self.__ABC__[c], transform(string.upper()))
            x = x_start
            for im in images:
                text_surface.blit(im, (x,y))
                x += tw
            y += th
        return text_surface
