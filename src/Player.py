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

CONST_JUMP_VELOCITY = 300
CONST_PLAYER_SPEED = 100


from enum import Enum
class PlayerState(Enum):
    GROUND = 0
    JUMPING = 1

class Player:
    def __init__(self, tiles, row, col, level):
        self.size = (BLOCK_SIZE, BLOCK_SIZE)

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
        self.collision_count = 0


        self.moving_component = MovingComponent(self.sprite, tiles, row, col)
        self.sprite.move(self.moving_component.position)
        self.level = level

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)

    def block_velocity(self,pos,target,tiles,col,row):
        for i in range(col):
            for j in range(row):
                if tiles[j][i]:
                    tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
                    target = src.Util.reduce_line2(pos, target, tile_rect)
        return target


    def get_displacement(self, position, displacement, tiles, row, col):
        target = (position[0] + displacement[0], position[1] + displacement[1])
        out1 = self.block_velocity(position, target, tiles, col, row)
        d = (out1[0] - position[0], out1[1] - position[1])
        return d

    def getrekt(self):
        return pygame.Rect(self.moving_component.position[0],self.moving_component.position[1],self.size[0],self.size[1])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.state==PlayerState.GROUND:
                self.moving_component.velocity = (self.moving_component.velocity[0],self.moving_component.velocity[1] - self.jump_velocity)
                self.state = PlayerState.JUMPING
                play_sound(SoundEnum.JUMP)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.moving_component.velocity = (0, self.moving_component.velocity[1])

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

    def handle_enemy_collisions(self):
        from src.Skeleton import Skeleton
        skeletons = self.level.monsters
        def lies_between(x, a, b):
            return a <= x <= b

        for skeleton in skeletons:
            assert(isinstance(skeleton, Skeleton))
            player_rect =self.sprite.sprite_rect()
            assert(isinstance(player_rect, pygame.Rect))

            other_rect = skeleton.sprite.sprite_rect()
            assert(isinstance(other_rect, pygame.Rect))

            collision = {}
            collision["right"] = lies_between(other_rect.left, player_rect.left, player_rect.right)
            collision["left"] = lies_between(other_rect.right, player_rect.left, player_rect.right)
            if collision["left"] or collision["right"]:
                collision["up"] = lies_between(other_rect.bottom, player_rect.top, player_rect.bottom)
                collision["down"] = lies_between(other_rect.top, player_rect.top, player_rect.bottom)
                if collision["down"] or collision["up"]:
                    self.collision_count = self.collision_count + 1








    def update(self, deltatime):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.moving_component.velocity = (-self.speed, self.moving_component.velocity[1])
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.moving_component.velocity = (self.speed, self.moving_component.velocity[1])
        else:
            self.moving_component.velocity = (0, self.moving_component.velocity[1])

        self.moving_component.update(deltatime)

        # print(self.moving_component.velocity)
        if not (self.moving_component.in_air):
            self.state = PlayerState.GROUND
            self.update_sprite()
        else:
            self.state = PlayerState.JUMPING
            self.update_sprite()

        self.sprite.update(deltatime)

        self.handle_enemy_collisions()
