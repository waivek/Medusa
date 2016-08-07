from src.AnimationFSM import AnimationFSM
from src.AnimatedSprite import AnimatedSprite
from src.LoadResources import ImageEnum
from src.WorldConstants import *
import pygame

from enum import Enum
class SkeletonState(Enum):
    GROUND = 0
    IN_AIR = 1
class Skeleton:
    def __init__(self):
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0,0)
        self.sprite = AnimationFSM()
        self.size = (BLOCK_SIZE, BLOCK_SIZE)
        spr0 = AnimatedSprite(ImageEnum.SKELETON_STANDING, 1)
        spr1 = AnimatedSprite(ImageEnum.SKELETON_WALKING, 10)
        self.sprite.add_sprite(spr0)
        self.sprite.add_sprite(spr1)
        self.sprite.state = 0
        self.state = SkeletonState.IN_AIR
        self.update_position((100, 10))


    def draw(self, screen):
        self.sprite.draw(screen)

    def update_position(self, displacement):
        self.sprite.move(displacement)
        newx = self.position[0] + int(displacement[0])
        newy = self.position[1] + int(displacement[1])
        self.position = (newx, newy)

    def set_acceleration(self,acc):
        self.acceleration=acc

    def update_velocity(self, acceleration):
        newx = self.velocity[0] + acceleration[0]
        newy = self.velocity[1] + acceleration[1]
        self.velocity = (newx, newy)

    def getrekt(self):
        return pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])

    def set_to_ground(self):
        self.state = SkeletonState.GROUND

    def update(self, deltaTime):
        dt = deltaTime / 1000
        self.update_position((self.velocity[0] * dt, self.velocity[1] * dt))
        self.update_velocity(((self.acceleration[0] * dt, self.acceleration[1] * dt)))
        if self.state == SkeletonState.IN_AIR:
            self.acceleration = (self.acceleration[0], CONST_GRAVITY)
        elif self.state == SkeletonState.GROUND:
            self.velocity = (self.velocity[0], 0)
            self.acceleration = (self.acceleration[0], 0)


