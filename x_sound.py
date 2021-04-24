import pygame
import os

from x_utils import XLoggingMixin


class XSoundManager(XLoggingMixin):
    class Channel:
        def __init__(self, m_channel, sound_manager):
            self.channel = m_channel
            self.sounds = sound_manager

        def play(self, name, *params, **kwargs):
            self.channel.play(self.sounds[name], *params, **kwargs)

        def fadeout(self, *params, **kwargs):
            self.channel.fadeout(*params, **kwargs)

    def __init__(self, sounds_dir):
        self.__class__.logger_setup()
        pygame.mixer.init(channels=2)

        self.sounds = dict()
        self.setup_sounds(sounds_dir)
        self.music = XSoundManager.Channel(pygame.mixer.Channel(0), self)
        self.effects = XSoundManager.Channel(pygame.mixer.Channel(1), self)

    def setup_sounds(self, sounds_dir):
        for sound_path in map(lambda p: os.path.join(sounds_dir, p), os.listdir(sounds_dir)):
            if os.path.isfile(sound_path):
                d, name = os.path.split(sound_path)
                name, ext = name.split('.')

                if ext in {'wav'}:
                    self.logger.info(name + '\t'+sound_path)
                    self.sounds[name] = pygame.mixer.Sound(sound_path)

    def __getitem__(self, item):
        return self.sounds[item]