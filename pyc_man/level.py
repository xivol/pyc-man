import pygame
from itertools import product

from pyc_man.actors import Ghost
from pyc_man.objects import Wall, Pellet, Energizer, Gate, BonusMixin, SpawnableMixin
from x_level import XTiledLevel
from x_object import XStaticObject
from tiled_renderer import TiledRenderer


class PycManLevel(XTiledLevel):
    __spawnpoint_type__ = 'spawnpoint'
    __blinking_layer__ = 'blink'

    __collider_types__ = {
        'wall': Wall,
        'pellet': Pellet,
        'power_pellet': Energizer,
        'gate': Gate
    }

    def __init__(self, filename):
        self.renderer = TiledRenderer(filename)
        super().__init__(self.renderer.tmx_data)

        self.spawnpoints = {}
        for obj in self.data.objects:
            if obj.type == self.__spawnpoint_type__:
                self.spawnpoints[obj.name] = (obj.x, obj.y)

        blinking_layer = self.data.get_layer_by_name(self.__blinking_layer__)
        if blinking_layer:
            self.blinking_layer = blinking_layer
            self.is_blinking = False
            self.time_since_blink = 0
            self.blink_duration = blinking_layer.properties['blink_duration']

    @property
    def pellets(self):
        return sum(1 for s in filter(lambda s: isinstance(s, Pellet) or isinstance(s, Energizer),
                              self.display_sprites))

    def draw(self, surface):
        self.renderer.render_map(surface)
        self.display_sprites.draw(surface)

    def setup_sprites(self, sprite_factory):
        p = product(range(self.data.width), range(self.data.height))
        coll_gids = set(self.colliders.data[y][x] for x, y in p)

        self.collider_sprites = pygame.sprite.Group()
        groups = {}
        for gid in coll_gids:
            try:
                props = self.data.tile_properties[gid]
                groups[props['type']] = group = pygame.sprite.Group()
                type = self.__collider_types__[props['type']]
            except KeyError:
                continue
            self.create_sprites(type, group,
                                sprite_factory, type.sprite_name(),
                                props['type'], self.colliders)

            self.collider_sprites.add(*group.sprites())

        self.display_sprites = pygame.sprite.Group()
        for g in map(lambda x: groups[x[0]],
                     filter(lambda x: issubclass(x[1], BonusMixin),
                            self.__collider_types__.items())):
            self.display_sprites.add(*g.sprites())

    def clear_sprites(self):
        self.display_sprites.empty()
        self.collider_sprites.empty()

    def stick_to_grid(self, position):
        tw = self.data.tilewidth
        th = self.data.tileheight
        return (position[0] // tw * tw + tw // 2,
                position[1] // th * th + th // 2)

    def wrap(self, x, y):
        width, height = self.renderer.pixel_size
        if not 0 <= x < width:
            x = (x + width) % width
        if not 0 <= y < height:
            y = (y + height) % height
        return x, y

    def can_pass(self, actor, direction):
        old_rect = actor.rect
        if actor.makes_turn:
            actor.rect.center = self.stick_to_grid(actor.rect.center)
        actor.rect = actor.rect.move(direction)
        collider = actor.get_hit(self.collider_sprites)
        actor.rect = old_rect
        return actor.behavior.can_pass(collider)

    def get_hit(self, actor):
        return actor.get_hit(self.collider_sprites)

    def remove(self, object):
        self.collider_sprites.remove(object)
        #if isinstance(object, BonusMixin):
        self.display_sprites.remove(object)
        if isinstance(object, SpawnableMixin):
            object.on_despawn(self)

    def spawn(self, object):
        position = self.spawnpoints[object.spawnpoint()]
        object.rect.center = position
        self.collider_sprites.add(object)
        self.display_sprites.add(object)
        return object

    def update(self, timedelta, *params):
        self.display_sprites.update(timedelta, *params)
        if self.is_blinking:
            self.blink(timedelta)

    def blink(self, timedelta):
        if not self.is_blinking:
            return
        self.time_since_blink += timedelta
        if self.time_since_blink >= self.blink_duration:
            self.blinking_layer.visible = not self.blinking_layer.visible
            self.time_since_blink = 0

    def set_blinking(self, is_blinking):
        if self.is_blinking != is_blinking:
            self.is_blinking = is_blinking
            self.time_since_blink = 0
            self.blinking_layer.visible = is_blinking



