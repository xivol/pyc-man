import math
import pygame
from tiled_renderer import TiledRenderer
from x_game import XGame
from x_object import XObject
from x_sprite_factory import XSpriteFactory

from pyc_man.objects import Pellet, Energizer, Fruits, Wall
from pyc_man.subjects import PacMan, Direction


def wrap(x, y, width, height):
    if not 0 <= x < width:
        x = (x + width) % width
    if not 0 <= y < height:
        y = (y + height) % height
    return x, y


class PycManGame(XGame):
    def __init__(self, screen_size, map_file, sprites_file):
        w, h = screen_size
        f = math.gcd(w, h)
        if w // f != 7 or h // f != 9:
            if h >= w:
                w = 7 * h // 9
            else:
                h = 9 * w // 7
        super().__init__('Pyc-Man', (w, h))

        self.renderer = TiledRenderer(map_file)
        self.map = self.renderer.tmx_data
        self.sprites = XSpriteFactory(sprites_file)
        self.load_map()
        self.load_actors()

        self.input.direction = None
        self.input.impact = None

    def load_actors(self):
        self.actors = pygame.sprite.Group()
        self.pacman = self.sprites['pacman-left'][0].make(PacMan,
                                                          self.spawnpoints['pacman'],
                                                          self.actors)

    def load_map(self):
        self.logger.info("Map Layers:")
        for l in self.map.layers:
            self.logger.info("%s", l)

        self.logger.info("Objects in map:")
        for obj in self.renderer.tmx_data.objects:
            self.logger.info(obj)
            for k, v in obj.properties.items():
                self.logger.info("%s\t%s", k, v)

        self.logger.info("GID (tile) properties:")
        for k, v in self.map.tile_properties.items():
            self.logger.info("%s\t%s", k, v)

        self.walls = pygame.sprite.Group()
        self.sprites['wall'] = {'gid': -1, 'width': 16, 'height': 16}
        self.load_map_objects(Wall, self.walls, 'wall',
                              'wall', 'collider')

        self.pellets = pygame.sprite.Group()
        self.load_map_objects(Pellet, self.pellets, Pellet.sprite_name(),
                              'pellet', 'collider')

        self.energizers = pygame.sprite.Group()
        self.load_map_objects(Energizer, self.energizers, Energizer.sprite_name(),
                              'power_pellet', 'collider')

        self.spawnpoints = {}
        for obj in self.renderer.tmx_data.objects:
            self.logger.info(obj)
            if obj.type == 'spawnpoint':
                self.spawnpoints[obj.name] = (obj.x, obj.y)

        self.bonus = pygame.sprite.Group()
        self.bonuses = [self.sprites[Fruits.sprite_name(i)].make(Fruits, order=i)
                        for i in range(Fruits.count())]

    def load_map_objects(self, type, group, sprite_name, tile_type, layer_name):
        gid, props = next(filter(lambda t: t[1]['type'] == tile_type,
                                 self.map.tile_properties.items()))
        if not props:
            raise Exception()

        layer = self.map.get_layer_by_name(layer_name)
        tw = self.map.tilewidth
        th = self.map.tileheight

        objects = []
        for x, y, gid in [i for i in layer.iter_data() if i[2] == gid]:
            pos = (tw * x + tw // 2, th * y + th // 2)
            obj = self.sprites[sprite_name].make(type, pos, group)
            objects.append(obj)

        return objects

    def has_wall(self, center, direction):
        x, y = direction.move(center, self.map.tilewidth // 2 + 1)
        x = x // self.map.tilewidth
        y = y // self.map.tileheight

        colliders = self.map.get_layer_by_name('collider')

        x,y = wrap(x, y, colliders.width, colliders.height)
        gid = colliders.data[y][x]
        props = self.map.get_tile_properties_by_gid(gid)

        return props and \
            (props['type'] == 'wall' or props['type'] == 'gate')


    def handle_input_event(self, event):
        super().handle_input_event(event)

        if event.type == pygame.KEYUP:
            self.input.direction = None

        if self.input.keys_pressed:
            if pygame.K_UP in self.input.keys_pressed:
                self.input.direction = Direction.UP
            elif pygame.K_DOWN in self.input.keys_pressed:
                self.input.direction = Direction.DOWN
            elif pygame.K_RIGHT in self.input.keys_pressed:
                self.input.direction = Direction.RIGHT
            elif pygame.K_LEFT in self.input.keys_pressed:
                self.input.direction = Direction.LEFT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.input.direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                self.input.direction = Direction.DOWN
            elif event.key == pygame.K_RIGHT:
                self.input.direction = Direction.RIGHT
            elif event.key == pygame.K_LEFT:
                self.input.direction = Direction.LEFT

    def draw(self, surface):
        temp = pygame.Surface(self.renderer.pixel_size)
        self.state.screen = temp
        self.renderer.render_map(temp)

        self.pellets.draw(temp)
        self.energizers.draw(temp)
        self.bonus.draw(temp)
        self.actors.draw(temp)

        pygame.transform.smoothscale(temp, surface.get_size(), surface)

    def update(self, timedelta):
        from pygame.sprite import spritecollideany

        self.input.impact = spritecollideany(self.pacman, self.pellets, XObject.collided)
        self.actors.update(timedelta, self.input, self.state)
        self.dirty = True
