from pygame import mixer
import os

from x_utils import XLoggingMixin


class XSoundManager(XLoggingMixin):
    def __init__(self, sounds_dir):
        self.__class__.logger_setup()
        self.sounds = dict()
        for sound_path in map(lambda p: os.path.join(sounds_dir, p), os.listdir(sounds_dir)):
            if os.path.isfile(sound_path):
                d, name = os.path.split(sound_path)
                name, ext = name.split('.')

                if ext in {'wav'}:
                    self.logger.info(name + '\t'+sound_path)
                    self.sounds[name] = mixer.Sound(sound_path)

    def __getitem__(self, item):
        return self.sounds[item]