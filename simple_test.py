import logging
from pprint import pprint

import pygame
from pygame.locals import *
import pytmx
from tiled_renderer import TiledRenderer
from x_game import XGame


class SimpleTest(XGame):
    """ Basic app to display a rendered Tiled map
    """

    def __init__(self, filename):
        super().__init__('PyTMX Map Viewer', (600,800))

        tsx = pytmx.load_pygame(filename, load_all=True)
        pprint(vars(tsx))

        self.logger.info("Testing %s", filename)

        self.load_map(filename)


    def load_map(self, filename):
        """ Create a renderer, load data, and print some debug info
        """
        self.renderer = TiledRenderer(filename)

        self.logger.info("Objects in map:")
        for obj in self.renderer.tmx_data.objects:
            self.logger.info(obj)
            for k, v in obj.properties.items():
                self.logger.info("%s\t%s", k, v)

        self.logger.info("GID (tile) properties:")
        for k, v in self.renderer.tmx_data.tile_properties.items():
            self.logger.info("%s\t%s", k, v)

        self.logger.info("Tile colliders:")
        for k, v in self.renderer.tmx_data.get_tile_colliders():
            self.logger.info("%s\t%s", k, list(v))

    def draw(self, surface):
        """ Draw our map to some surface (probably the display)
        """
        # first we make a temporary surface that will accommodate the entire
        # size of the map.
        # because this demo does not implement scrolling, we render the
        # entire map each frame
        temp = pygame.Surface(self.renderer.pixel_size)

        # render the map onto the temporary surface
        self.renderer.render_map(temp)

        # now resize the temporary surface to the size of the display
        # this will also 'blit' the temp surface to the display
        pygame.transform.smoothscale(temp, surface.get_size(), surface)

        # display a bit of use info on the display
        f = pygame.font.Font(pygame.font.get_default_font(), 20)
        i = f.render('press any key for next map or ESC to quit',
                     1, (180, 180, 0))
        surface.blit(i, (0, 0))

    def handle_input_event(self, event):
            if event.type == QUIT:
                self.exit_status = 0
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exit_status = 0
                    self.running = False
                else:
                    self.running = False

            elif event.type == VIDEORESIZE:
                XGame.init_screen(event.w, event.h)
                self.dirty = True


