from src.MovingComponent import *
from src.AnimatedSprite import *

class Projectile:
    def __init__(self, spriteenum, pos, velocity, level, start_func, update_func, collide_func):
        self.sprite = AnimatedSprite(spriteenum,1)

        self.moving_component = MovingComponent(self.sprite,level.map,level.col,level.row)
        self.moving_component.move(pos)
        self.moving_component.velocity = velocity

        self.start_func = start_func
        self.update_func = update_func
        self.collide_func = collide_func

        self.start_func(self)

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.moving_component.update(deltatime)
        self.update_func(self)