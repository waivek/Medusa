from src.AnimationFSM import AnimationFSM
from src.AnimatedSprite import AnimatedSprite
from src.LoadResources import ImageEnum
from src.MovingComponent import MovingComponent
from src.EnemyMovementComponent import EnemyMovementComponent
from src.Health import *
import pygame

from enum import Enum

class SkeletonState(Enum):
    GROUND = 0
    IN_AIR = 1

class Skeleton:
    def __init__(self, pos, level):
        self.sprite = AnimationFSM()
        self.level = level
        spr0 = AnimatedSprite(ImageEnum.SKELETON_STANDING, 1)
        spr1 = AnimatedSprite(ImageEnum.SKELETON_WALKING, 10)
        self.sprite.add_sprite(spr0)
        self.sprite.add_sprite(spr1)
        self.sprite.state = 0
        self.state = SkeletonState.IN_AIR
        self.moving_component = MovingComponent(self, self.level)
        self.moving_component.update_position(pos)
        self.enemy_movement_component = EnemyMovementComponent(self.moving_component, self.level)
        self.health = 1

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)

    def getrekt(self):
        return pygame.Rect(self.moving_component.position[0],self.moving_component.position[1],self.moving_component.size[0],self.moving_component.size[1])

    def set_to_ground(self):
        self.state = SkeletonState.GROUND

    def update_sprite(self):
        if (self.moving_component.in_air):
            self.sprite.set_state(0)
        else:
            self.sprite.set_state(1)

    def update(self, deltaTime):
        self.moving_component.update(deltaTime)
        self.enemy_movement_component.update(deltaTime)

        if self.health <= 0:
            self.level.destroy_entity(self)

        self.sprite.update(deltaTime)
        self.update_sprite()

    def save(self, file):
        file.write(str(self.moving_component.position[0]))
        file.write('\n')
        file.write(str(self.moving_component.position[1]))
        file.write('\n')

    @staticmethod
    def load(file, level):
        posx = int(file.readline())
        posy = int(file.readline())
        pos = (posx,posy)
        return (Skeleton(pos, level))