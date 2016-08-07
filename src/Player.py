from src.AnimationFSM import AnimationFSM
from src.AnimatedSprite import AnimatedSprite
from src.LoadResources import SoundEnum
from src.LoadResources import play_sound
from src.LoadResources import ImageEnum

import pygame

BLOCK_SIZE = 32

CONST_GRAVITY = 500
CONST_JUMP_VELOCITY = 500
CONST_PLAYER_SPEED = 100

from enum import Enum
class PlayerState(Enum):
    GROUND = 0
    JUMPING = 1

class Player:
    def __init__(self):
        self.size = (BLOCK_SIZE, BLOCK_SIZE)
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0,0)
        self.state = PlayerState.JUMPING

        self.speed = CONST_PLAYER_SPEED
        self.jump_velocity = CONST_JUMP_VELOCITY

        self.sprite = AnimationFSM()
        spr0 = AnimatedSprite(ImageEnum.PLAYER1_RIGHT, 8)
        spr1 = AnimatedSprite(ImageEnum.PLAYER1_LEFT, 8)
        spr2 = AnimatedSprite(ImageEnum.PLAYER1_JUMPRIGHT, 1)
        spr3 = AnimatedSprite(ImageEnum.PLAYER1_JUMPLEFT, 1)
        spr4 = AnimatedSprite(ImageEnum.PLAYER1_RIGHT, 1)
        spr5 = AnimatedSprite(ImageEnum.PLAYER1_LEFT, 1)
        self.sprite.add_sprite(spr0)
        self.sprite.add_sprite(spr1)
        self.sprite.add_sprite(spr2)
        self.sprite.add_sprite(spr3)
        self.sprite.add_sprite(spr4)
        self.sprite.add_sprite(spr5)

        self.sprite.set_state(2)

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)

    def update_position(self, displacement):
        self.sprite.move(displacement)
        newx = self.position[0] + int(displacement[0])
        newy = self.position[1] + int(displacement[1])
        self.position = (newx, newy)

    def update_velocity(self, acceleration):
        newx = self.velocity[0] + acceleration[0]
        newy = self.velocity[1] + acceleration[1]
        self.velocity = (newx, newy)

    def getpos(self):
        return self.position

    def getrekt(self):
        return pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.velocity = (-self.speed, self.velocity[1])
            if event.key == pygame.K_RIGHT:
                self.velocity = (self.speed, self.velocity[1])
            if event.key == pygame.K_SPACE and self.state==PlayerState.GROUND:
                self.velocity = (self.velocity[0],self.velocity[1] - self.jump_velocity)
                self.state = PlayerState.JUMPING
                play_sound(SoundEnum.JUMP)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.velocity = (0, self.velocity[1])

    def set_acceleration(self,acc):
        self.acceleration=acc

    def update(self, deltatime):
        dt = deltatime / 1000

        print(self.velocity)

        #update parameters
        self.update_position((self.velocity[0] * dt, self.velocity[1] * dt))
        self.update_velocity(((self.acceleration[0] * dt, self.acceleration[1] * dt)))

        #update state
        if self.state == PlayerState.JUMPING:
            self.acceleration = (self.acceleration[0], CONST_GRAVITY)
        elif self.state == PlayerState.GROUND:
            self.velocity = (self.velocity[0], 0)
            self.acceleration = (self.acceleration[0], 0)

        #update sprite
        self.sprite.update(deltatime)
        if(self.state==PlayerState.JUMPING):
            if self.velocity[0]>0:
                self.sprite.set_state(2)
            else:
                self.sprite.set_state(3)
        else:
            if (self.velocity[0] > 0):
                self.sprite.set_state(0)
            elif self.velocity[0] < 0:
                self.sprite.set_state(1)
            else:
                if self.sprite.state == 0:
                    self.sprite.set_state(4)
                if self.sprite.state == 1:
                    self.sprite.set_state(5)