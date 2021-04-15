
class XTiledLevel:
    __colliders_layer__ = 'collider'
    __navigation_layer__ = 'nav'

    def __init__(self, tmx_data):
        self.data = tmx_data
        self.colliders = self.data.get_layer_by_name(self.__colliders_layer__)
        self.navigation = self.data.get_layer_by_name(self.__navigation_layer__)

        self.width = tmx_data.width
        self.tile_width = tmx_data.tilewidth
        self.height = tmx_data.height
        self.tile_height = tmx_data.tileheight


    def create_sprites(self, type, group, sprite_factory, sprite_name, tile_type, layer):
        gid, props = next(filter(lambda t: t[1]['type'] == tile_type,
                                 self.data.tile_properties.items()))
        if not props:
            raise Exception()

        try:
            sprite_factory[sprite_name]
        except KeyError:
            ts = self.data.get_tileset_from_gid(gid)
            sprite_factory.add(sprite_name, gid=-1, width=ts.tilewidth, height=ts.tileheight)

        tw = self.data.tilewidth
        th = self.data.tileheight
        for x, y, gid in [i for i in layer.iter_data() if i[2] == gid]:
            pos = (tw * x + tw // 2, th * y + th // 2)
            obj = sprite_factory[sprite_name].make(type, pos, group)
