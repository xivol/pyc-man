import math



def dimensions(w, h):
    f = math.gcd(w, h)
    if w // f != 7 or h // f != 9:
        if h >= w:
            w = 7 * h // 9
        else:
            h = 9 * w // 7
    return w, h


if __name__ == '__main__':
    import sys
    import os.path
    import logging
    import pygame

    from pyc_man.game_state import InitState, WinState, LoseState, ReadyState
    from pyc_man.game_state import ChaseState, FrightState
    from x_game import XGame

    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)

    logging.basicConfig(level=logging.DEBUG)

    try:
        game = XGame('Pyc-Man', dimensions(600, 800), os.path.join('data', 'img', 'pacman_icon_title.ico'))
        game_states = {"Init": InitState(os.path.join('data', 'level_01.tmx'),
                                         os.path.join('data', 'sprites.tmx'),
                                         os.path.join('data', 'font.tmx'),
                                         os.path.join('data', 'snd'),
                                         'Ready'),
                       "Ready": ReadyState('Chase', 'Player One', 'Ready!'),
                       "Chase": ChaseState(),
                       "Fright": FrightState(5, 3),
                       "Win":  WinState('Next Level', 'Chase'),
                       "Lose": LoseState('Uh-Oh!', pygame.Color(255, 184, 81), 'Chase'),
                       "GameOver": LoseState("Game Over!", pygame.Color(255, 0, 0), 'Init')
        }
        game.setup_states(game_states, "Init")
        game.run()
    except:
        pygame.quit()
        raise