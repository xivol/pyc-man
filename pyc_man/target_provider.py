from. import actors


class TargetProvider:
    def get_target(self, world):
        pacman = world.pacman
        return pacman.rect.center
