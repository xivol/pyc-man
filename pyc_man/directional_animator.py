from x_animation import AnimationManager
from x_input import Direction
from itertools import product


class DirectionalAnimationManager(AnimationManager):
    def __init__(self, sprite_name, sprites, anim_dict, init_state, init_direction=Direction.default()):
        self.direction = init_direction
        super().__init__(sprite_name, sprites, anim_dict, init_state)

    def __make_animation__(self, sprites, anim_name, anim_type):
        if anim_name in sprites:
            return super().__make_animation__(sprites, anim_name, anim_type)
        else:
            dirs = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
            dir_names = map(lambda x: '-'.join(x),
                            product([anim_name], map(str, dirs)))
            dir_anims = dict()
            for direction, name in zip(dirs, dir_names):
                dir_anims[direction] = super().__make_animation__(sprites, name, anim_type)
            return dir_anims

    def __get_state_animation__(self):
        if isinstance(self.animations[self.state], dict):
            return self.animations[self.state][self.direction]
        else:
            return super().__get_state_animation__()

    def set_direction(self, new_direction):
        if self.direction != new_direction:
            self.direction = new_direction
            self.change_animation()