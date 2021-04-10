



if __name__ == '__main__':
    import os.path
    import logging
    from pyc_man.game import PycManGame
    import pygame

    logging.basicConfig(level=logging.DEBUG)

    try:
        PycManGame((600, 800),
                   os.path.join('data', 'level_01.tmx'),
                   os.path.join('data', 'sprites.tmx'))\
            .run()
    except:
        pygame.quit()
        raise