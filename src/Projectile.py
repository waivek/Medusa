from src.MovingComponent import *
from src.AnimatedSprite import *

class Projectile:
    def __init__(self, spriteenum, pos, velocity, gravity, bounciness, collides, level):
        self.sprite = AnimatedSprite(spriteenum,1)

        self.moving_component = MovingComponent(self.sprite,level.tileslevel.col,level.row)
        self.moving_component.move(pos)
        self.moving_component.velocity = velocity

        self.moving_component.gravity = gravity
        self.moving_component.bounciness = bounciness
        self.moving_component.collides = collides

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.moving_component.update(deltatime)