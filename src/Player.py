from src.AnimationFSM import AnimationFSM
from src.AnimatedSprite import AnimatedSprite
from src.LoadResources import SoundEnum
from src.LoadResources import play_sound
from src.LoadResources import ImageEnum
from src.MovingComponent import *
import src.Util

import pygame

BLOCK_SIZE = 32
CONST_CAMERA_PLAYER_OFFSET = 160

CONST_GRAVITY = 500
CONST_JUMP_VELOCITY = 500
CONST_PLAYER_SPEED = 100
CONST_MAX_VELOCITY = 500

from enum import Enum
class PlayerState(Enum):
    GROUND = 0
    JUMPING = 1

class Player:
    def __init__(self):
        self.moving_component = MovingComponent()

        self.size = (BLOCK_SIZE, BLOCK_SIZE)
        self.position = (CONST_CAMERA_PLAYER_OFFSET, CONST_CAMERA_PLAYER_OFFSET)
        self.velocity = (0, 0)
        self.acceleration = (0,0)

        self.oldvelocity = (0,0)
        self.oldposition = (0,0)

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
        self.sprite.move(self.position)

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)

    def block_velocity(self,pos,target,tiles,col,row):
        for i in range(col):
            for j in range(row):
                if tiles[j][i]:
                    tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
                    #tile_rect.bottomright = (BLOCK_SIZE*i +32,BLOCK_SIZE*j +32)
                    t_x = target[0]
                    t_y = target[1]
                    target = src.Util.reduce_line2(pos, target, tile_rect)

                    if((t_x,t_y) != target):
                        print("new target: %d %d" % (i,j))
                        print(target)
                        #print(tile_rect)
        return target


    def get_displacement(self, position, displacement, tiles, row, col):
        target = (position[0] + displacement[0], position[1] + displacement[1])
        out1 = self.block_velocity(position, target, tiles, col, row)
        d = (out1[0] - position[0], out1[1] - position[1])
        return d

    def move(self, displacement):
        self.sprite.move(displacement)
        print("displ")
        print(displacement)
        print(self.position)
        newx = self.position[0] + int(displacement[0])
        newy = self.position[1] + int(displacement[1])
        self.position = (newx, newy)
        print(self.position)

    def update_position(self, displacement, tiles, col, row):
        displacement = (int(displacement[0]),int(displacement[1]))

        #check for collisions
        # d1 = self.get_displacement(self.sprite.sprite_rect().topleft, displacement, tiles, row, col)
        # d2 = self.get_displacement(self.sprite.sprite_rect().topright, displacement, tiles, row, col)
        # d3 = self.get_displacement(self.sprite.sprite_rect().bottomleft, displacement, tiles, row, col)
        # d4 = self.get_displacement(self.sprite.sprite_rect().bottomright, displacement, tiles, row, col)
        #
        # print("d1")
        # print(self.sprite.sprite_rect().topleft)
        # print("d2")
        # print(self.sprite.sprite_rect().topright)
        # print("d3")
        # print(self.sprite.sprite_rect().bottomleft)
        # print("d4")
        # print(self.sprite.sprite_rect().bottomright)
        # dx = min([d1[0],d2[0],d3[0],d4[0]])
        # dy = min([d1[1],d2[1],d3[1],d4[1]])
        #
        #
        # dis_old = displacement
        #
        # displacement = (dx,dy)
        # #print("displacement")
        # #print(displacement)
        #
        # if(dis_old[0]!=displacement[0]):
        #     self.velocity = (0, self.velocity[1])
        #     print("player rect")
        #     print(self.sprite.sprite_rect())
        #
        # if(dis_old[1]!=displacement[1]):
        #     self.velocity = (self.velocity[0], 1)
        #     print("player rect")
        #     print(self.sprite.sprite_rect())
        #update position
        self.sprite.move(displacement)
        newx = self.position[0] + int(displacement[0])
        newy = self.position[1] + int(displacement[1])
        self.position = (newx, newy)

        self.snap_out(tiles,col,row)

        if(abs(displacement[1])<=1):
            self.state = PlayerState.GROUND
            self.update_sprite()
        else:
            self.state = PlayerState.JUMPING
            self.update_sprite()

    def update_velocity(self, acceleration):
        newx = self.velocity[0] + acceleration[0]
        newy = self.velocity[1] + acceleration[1]

        #cap the velocity
        if(newx>CONST_MAX_VELOCITY):
            newx = CONST_MAX_VELOCITY
        if(newy>CONST_MAX_VELOCITY):
            newy=CONST_MAX_VELOCITY

        self.velocity = (newx, newy)

    def getpos(self):
        return self.position

    def getrekt(self):
        return pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_LEFT:
                #self.velocity = (-self.speed, self.velocity[1])
            #if event.key == pygame.K_RIGHT:
                #self.velocity = (self.speed, self.velocity[1])
            if event.key == pygame.K_SPACE and self.state==PlayerState.GROUND:
                self.velocity = (self.velocity[0],self.velocity[1] - self.jump_velocity)
                self.state = PlayerState.JUMPING
                play_sound(SoundEnum.JUMP)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.velocity = (0, self.velocity[1])

    def set_acceleration(self,acc):
        self.acceleration=acc

    def update_sprite(self):
        if (self.state == PlayerState.JUMPING):
            if self.velocity[0] >= 0:
                self.sprite.set_state(2)
            else:
                self.sprite.set_state(3)
        else:
            if self.velocity[0] > 0:
                self.sprite.set_state(0)
            elif self.velocity[0] < 0:
                self.sprite.set_state(1)
            else:
                if self.sprite.state == 0 or self.sprite.state==2:
                    self.sprite.set_state(4)
                if self.sprite.state == 1 or self.sprite.state==3:
                    self.sprite.set_state(5)

    def update(self, deltatime, tiles, col, row):
        dt = deltatime / 1000
        print(self.position)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.velocity = (-self.speed, self.velocity[1])
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.velocity = (self.speed, self.velocity[1])
        else:
            self.velocity = (0, self.velocity[1])

        #update parameters
        self.oldposition = self.position
        self.update_position((self.velocity[0] * dt, self.velocity[1] * dt), tiles, col, row)
        self.oldvelocity = self.velocity
        self.update_velocity(((self.acceleration[0] * dt, self.acceleration[1] * dt)))

        #update state
        #if self.state == PlayerState.JUMPING:
        self.acceleration = (self.acceleration[0], CONST_GRAVITY)
        #elif self.state == PlayerState.GROUND:
        #    self.velocity = (self.velocity[0], 0)
        #    self.acceleration = (self.acceleration[0], 0)

        #update sprite
        #print(self.state)
        self.sprite.update(deltatime)
        self.update_sprite()
        #print(self.position)
        #print(self.velocity)

        #assert(self.position == self.sprite.sprite_rect().topleft)
