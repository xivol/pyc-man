from abc import abstractmethod

import pygame
import os

from x_utils import XLoggingMixin


class XSoundMixin:
    def __init__(self):
        self.sounds = dict()

    def setup_sounds(self, sound_manager, sound_dict):
        for key, name in sound_dict.items():
            self.sounds[key] = sound_manager[name]

    @abstractmethod
    def play_sound(self, sound, channel):
        pass

    def stop_sound(self, channel):
        if channel.sound():
            channel.sound().stop()


class XSoundManager(XLoggingMixin):
    class Channel:
        def __init__(self, id, sound_manager):
            self.channel = pygame.mixer.Channel(id)
            self.sounds = sound_manager

        def __get_sound__(self, sound):
            if isinstance(sound, str):
                return self.sounds[sound]
            else:
                return sound

        def play(self, sound, *params, **kwargs):
            self.channel.play(self.__get_sound__(sound), *params, **kwargs)

        def fadeout(self, *params, **kwargs):
            sound = self.channel.get_sound()
            if sound:
                sound.fadeout(*params, **kwargs)

        def is_busy(self):
            return self.channel.get_busy()

        def sound(self):
            return self.channel.get_sound()

        def enqueue(self, sound):
            self.channel.queue(self.__get_sound__(sound))

    def __init__(self, sounds_dir, channels):
        self.__class__.logger_setup()
        self.sounds = dict()
        self.setup_sounds(sounds_dir)
        self.channels = None
        self.setup_channels(channels)

    def setup_channels(self, channels):
        pygame.mixer.init(channels=len(channels))

        self.channels = {name: XSoundManager.Channel(i, self)
                         for i, name in enumerate(channels)}

        for name in channels:
            self.__setattr__(name.lower(), self.channels[name])

    def channel(self, key):
        return self.channels[key]

    def setup_sounds(self, sounds_dir):
        for sound_path in map(lambda p: os.path.join(sounds_dir, p), os.listdir(sounds_dir)):
            if os.path.isfile(sound_path):
                d, name = os.path.split(sound_path)
                name, ext = name.split('.')

                if ext in {'wav'}:
                    self.logger.info(name + '\t' + sound_path)
                    self.sounds[name] = pygame.mixer.Sound(sound_path)

    def __getitem__(self, item):
        return self.sounds[item]
