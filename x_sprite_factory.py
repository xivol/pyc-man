import logging
import pygame
import pytmx

from x_utils import XLoggingMixin


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


class AnimationData(SpriteData):
    def __init__(self, gid, name, image, width, height):
        super().__init__(gid, name, image, width, height)

        self.frames = []
        self.durations = []

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, item):
        return self.frames[item]

    def append(self, frame, duration):
        self.frames.append(frame)
        self.durations.append(duration)

    def make(self, type, *params, **kwargs):
        if len(self.frames) == 1:
            return type(self.frames[0],
                        self.durations[0],
                        *params, **kwargs)
        return type(self.frames,
                    self.durations,
                    *params, **kwargs)


class XSpriteFactory(XLoggingMixin):
    @staticmethod
    def anim_sprite_names(sprite_name, anim_dict):
        return map(lambda state: '-'.join((sprite_name, state)), anim_dict.keys())

    def __init__(self, logger=None):
        super().__init__(logger)
        self.sprites = dict()

    def __getitem__(self, item):
        return self.sprites[item]

    def add(self, key, **value):
        if key in self.sprites:
            raise Exception()

        image = value.get('image', pygame.Surface((value['width'], value['height'])))
        if 'frames' in value:
            frames = value['frames']
            durations = value['durations']
            anim = AnimationData(value['gid'], key, image, value['width'], value['height'])
            for i in range(len(frames)):
                anim.append(frames[i], durations[i])
            self.sprites[key] = anim
        else:
            self.sprites[key] = SpriteData(value['gid'], key, image, value['width'], value['height'])


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
                result[props['type']] = self.get_images(gid, props['type'],
                                                        props['width'], props['height'],
                                                        props['frames'])
        return result

    def get_images(self, gid, type, width, height, frames):
        if frames:
            anim = AnimationData(gid, type, self.tmx_data.get_tile_image_by_gid(gid),
                                 width, height)
            for i, frame in enumerate(frames):
                sd = SpriteData(frame.gid, '-'.join(type.split('-') + [str(i)]),
                                self.tmx_data.get_tile_image_by_gid(frame.gid),
                                width, height)
                anim.append(sd, frame.duration)
            return anim
        else:
            sd = SpriteData(gid, type, self.tmx_data.get_tile_image_by_gid(gid),
                            width, height)
            return sd
