from src.AnimationFSM import AnimationFSM
from src.AnimatedSprite import AnimatedSprite
from src.LoadResources import SoundEnum
from src.LoadResources import play_sound
from src.LoadResources import ImageEnum

import pygame

from src.MovingComponent import MovingComponent

BLOCK_SIZE = 32
CONST_CAMERA_PLAYER_OFFSET = 160

CONST_GRAVITY = 500
CONST_JUMP_VELOCITY = 500
CONST_PLAYER_SPEED = 100

from enum import Enum
class PlayerState(Enum):
    GROUND = 0
    JUMPING = 1

class Player:
    def __init__(self):
        # self.moving_component.size = (BLOCK_SIZE, BLOCK_SIZE)
        # self.moving_component.position = (CONST_CAMERA_PLAYER_OFFSET, CONST_CAMERA_PLAYER_OFFSET)
        # self.moving_component.velocity = (0, 0)
        # self.moving_component.acceleration = (0,0)
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

        self.moving_component = MovingComponent(self.sprite)
        self.moving_component.update_position((CONST_CAMERA_PLAYER_OFFSET, CONST_CAMERA_PLAYER_OFFSET))

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)

    def getpos(self):
        return self.moving_component.position

    def getrekt(self):
        return pygame.Rect(self.moving_component.position[0],self.moving_component.position[1],self.moving_component.size[0],self.moving_component.size[1])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_LEFT:
                #self.moving_component.velocity = (-self.speed, self.moving_component.velocity[1])
            #if event.key == pygame.K_RIGHT:
                #self.moving_component.velocity = (self.speed, self.moving_component.velocity[1])
            if event.key == pygame.K_SPACE and self.state==PlayerState.GROUND:
                self.moving_component.velocity = (self.moving_component.velocity[0],self.moving_component.velocity[1] - self.jump_velocity)
                self.state = PlayerState.JUMPING
                play_sound(SoundEnum.JUMP)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.moving_component.velocity = (0, self.moving_component.velocity[1])


    def set_acceleration(self,acc):
        self.moving_component.acceleration=acc

    def update_sprite(self):
        if (self.state == PlayerState.JUMPING):
            if self.moving_component.velocity[0] >= 0:
                self.sprite.set_state(2)
            else:
                self.sprite.set_state(3)
        else:
            if self.moving_component.velocity[0] > 0:
                self.sprite.set_state(0)
            elif self.moving_component.velocity[0] < 0:
                self.sprite.set_state(1)
            else:
                if self.sprite.state == 0 or self.sprite.state==2:
                    self.sprite.set_state(4)
                if self.sprite.state == 1 or self.sprite.state==3:
                    self.sprite.set_state(5)

    def update(self, deltatime):
        dt = deltatime / 1000

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.moving_component.velocity = (-self.speed, self.moving_component.velocity[1])
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.moving_component.velocity = (self.speed, self.moving_component.velocity[1])
        else:
            self.moving_component.velocity = (0, self.moving_component.velocity[1])
        #update parameters
        self.moving_component.update_position((self.moving_component.velocity[0] * dt, self.moving_component.velocity[1] * dt))
        self.moving_component.update_velocity(((self.moving_component.acceleration[0] * dt, self.moving_component.acceleration[1] * dt)))

        #update state
        #if self.state == PlayerState.JUMPING:
        self.moving_component.acceleration = (self.moving_component.acceleration[0], CONST_GRAVITY)
        #elif self.state == PlayerState.GROUND:
        #    self.moving_component.velocity = (self.moving_component.velocity[0], 0)
        #    self.moving_component.acceleration = (self.moving_component.acceleration[0], 0)

        #update sprite
        print(self.state)
        print(self.moving_component.position)
        self.sprite.update(deltatime)
        self.update_sprite()
