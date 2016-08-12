from src.AnimationFSM import AnimationFSM
from src.AnimatedSprite import AnimatedSprite
from src.LoadResources import ImageEnum
from src.WorldConstants import *
from src.MovingComponent import MovingComponent
from src.EnemyMovementComponent import EnemyMovementComponent
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
        self.moving_component = MovingComponent(self.sprite, level.tiles, level.col, level.row)
        self.moving_component.update_position(pos)
        self.enemy_movement_component = EnemyMovementComponent(self.moving_component, self.level)

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
        self.sprite.update(deltaTime)
        self.update_sprite()

