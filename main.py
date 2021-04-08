import logging

import pygame

from simple_test import SimpleTest




if __name__ == '__main__':
    import os.path
    import glob

    logging.basicConfig(level=logging.DEBUG)

    # loop through a bunch of maps in the maps folder
    try:
        for filename in glob.glob(os.path.join('data', '*.tmx')):
            test = SimpleTest(filename)

            if not test.run():
                break
    except:
        pygame.quit()
        raise