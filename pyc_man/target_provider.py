from. import actors


class TargetProvider:
    def get_target(self, world):
        pacman = next(filter(lambda a: isinstance(a, actors.PacMan), world.actors))
        return pacman.rect.center
