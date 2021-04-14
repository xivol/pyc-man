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
    import os.path
    import logging
    import pygame

    from pyc_man.game_state import InitState, WinState, LoseState
    from pyc_man.game_state import RunningState
    from x_game import XGame

    logging.basicConfig(level=logging.DEBUG)

    try:
        game = XGame('Pyc-Man', dimensions(600, 800))
        game_states = {"Init": InitState(os.path.join('data', 'level_01.tmx'),
                                         os.path.join('data', 'sprites.tmx'),
                                         os.path.join('data', 'font.tmx')),
                       "Running": RunningState(),
                       "Win":  WinState('press start to continue'),
                       "Lose": LoseState('press start to continue')
        }
        game.setup_states(game_states, "Init")
        game.run()
    except:
        pygame.quit()
        raise