import logging
import pygame
import pytmx


class SpriteData:
    def __init__(self, gid, name, image, width, height):
        self.image = image
        self.gid = gid
        self.name = name
        self.size = (width, height)

    def make(self, type, *params, **kwargs):
        if not issubclass(type, pygame.sprite.Sprite):
            raise Exception()
        return type(self.image,
                    pygame.Rect((0, 0), self.size),
                    *params, **kwargs)


class XSpriteFactory:
    @classmethod
    def logger_setup(cls, logger=None):
        if not logger:
            cls.logger = logging.getLogger(cls.__name__)
        else:
            cls.logger = logger

    def __init__(self, filename, logger=None):
        if 'logger' not in self.__class__.__dict__:
            self.__class__.logger_setup(logger)
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
                result[props['type']] = self.get_images(gid, props['type'],
                                                        props['width'], props['height'],
                                                        props['frames'])
        return result

    def get_images(self, gid, type, width, height, frames):
        if frames:
            anim = []
            for i, frame in enumerate(frames):
                sd = SpriteData(frame.gid, '-'.join(type.split('-')+[str(i)]),
                                self.tmx_data.get_tile_image_by_gid(frame.gid),
                                width, height)
                anim.append(sd)
            return anim
        else:
            sd = SpriteData(gid, type, self.tmx_data.get_tile_image_by_gid(gid),
                            width, height)
            return sd

    def __getitem__(self, item):
        return self.sprites[item]

    def __setitem__(self, key, value):
        if key in self.sprites:
            raise Exception()

        image = value.get('image', pygame.Surface((value['width'], value['height'])))
        self.sprites[key] = SpriteData(value['gid'], key, image, value['width'], value['height'])
