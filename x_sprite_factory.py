import pygame
import pytmx

from x_utils import XLoggingMixin


class SpriteData:
    def __init__(self, gid, name, image, width, height, **kwargs):
        self.image = image
        self.gid = gid
        self.name = name
        self.size = (width, height)
        self.frames = kwargs.get('frames', None)
        self.looping = kwargs.get('looping', False)

    def is_animated(self):
        return self.frames is not None

    def make(self, type, *params, **kwargs):
        if not issubclass(type, pygame.sprite.Sprite):
            raise Exception()
        return type(self.image,
                    pygame.Rect((0, 0), self.size),
                    *params, **kwargs)


class XSpriteFactory(XLoggingMixin):
    @staticmethod
    def anim_sprite_names(sprite_name, anim_dict):
        return map(lambda state: '-'.join((sprite_name, state)), anim_dict.keys())

    def __init__(self, logger=None):
        self.__class__.logger_setup(logger)
        self.sprites = dict()

    def __getitem__(self, item):
        return self.sprites.__getitem__(item)

    def __contains__(self, item):
        return self.sprites.__contains__(item)

    def add(self, key, **value):
        if key in self.sprites:
            raise Exception()

        image = value.pop('image', pygame.Surface((value['width'], value['height'])))
        self.sprites[key] = SpriteData(value.pop('gid'), key, image, \
                                       value.pop('width'), value.pop('height'), **value)


class XTMXSpriteFactory(XSpriteFactory):
    def __init__(self, filename, logger=None):
        super().__init__(logger)
        self.tmx_data = pytmx.load_pygame(filename, load_all=True)
        self.sprites = self.load_sprites()

    def load_sprites(self):
        result = {}
        self.logger.info("Sprites Layers:")
        for l in self.tmx_data.layers:
            self.logger.info("%s", l)

        for gid, props in self.tmx_data.tile_properties.items():
            self.logger.info("\t%s\t%s", gid, props)
            if props['type']:
                type = props.pop('type')
                width= props.pop('width')
                height = props.pop('height')
                result[type] = SpriteData(gid, type, self.get_raw_image(gid),
                                                   width, height, **props)
        return result

    def get_raw_image(self, gid):
        return self.tmx_data.get_tile_image_by_gid(gid)
