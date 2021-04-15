import pygame

import x_object
from x_sprite_factory import SpriteData
from x_utils import XLoggingMixin


class AnimationData(SpriteData):
    def __init__(self, gid, name, image, width, height, looping):
        super().__init__(gid, name, image, width, height)

        self.frames = []
        self.durations = []
        self.looping = looping

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, item):
        return self.frames[item]

    def append(self, frame, duration):
        self.frames.append(frame)
        self.durations.append(duration)

    def make(self, type, *params, **kwargs):
        if len(self.frames) == 0:
            return type(self.image, *params, **kwargs)
        if len(self.frames) == 1:
            return type(self.frames[0], self.durations[0],
                        *params, **kwargs)
        return type(self.frames, self.durations, is_looping=self.looping,
                    *params, **kwargs)


class XAnimationFactory(XLoggingMixin):
    @staticmethod
    def anim_sprite_names(sprite_name, anim_dict):
        return map(lambda state: '-'.join((sprite_name, state)), anim_dict.keys())

    @staticmethod
    def core_sprite_name(anim_name):
        return '-'.join(anim_name.split('-')[:-1])

    def __init__(self, sprite_factory, logger=None):
        self.__class__.logger_setup(logger)
        self.animations = dict()
        self.sprites = sprite_factory
        self.load_animations(sprite_factory)

    def load_animations(self, sprite_factory):
        anims = filter(lambda x: x.is_animated(), sprite_factory.sprites.values())
        for sprite in anims:
            anim = AnimationData(sprite.gid, sprite.name, sprite.image,
                                 sprite.size[0], sprite.size[1], sprite.looping)
            for frame in sprite.frames:
                img = sprite_factory.get_raw_image(frame.gid)
                anim.append(img, frame.duration)
            self.animations[sprite.name] = anim

    def __getitem__(self, item):
        return self.animations.__getitem__(item)

    def __contains__(self, item):
        return self.animations.__contains__(item)

    def add(self, key, **value):
        if key in self.animations:
            raise Exception()

        image = value.get('image', pygame.Surface((value['width'], value['height'])))
        frames = value['frames']
        durations = value['durations']
        anim = AnimationData(value['gid'], key, image, value['width'], value['height'], value.get('looping', False))
        for i in range(len(frames)):
            anim.append(frames[i], durations[i])
        self.animations[key] = anim

    def make(self, type, *params, **kwargs):
        if not issubclass(type, x_object.XAnimatedObject):
            raise Exception
        man = type.__manager_type__(type.__sprite_name__,
                                    self,
                                    type.__animations__,
                                    type.__default_state__)
        return type(man, *params, **kwargs)
