from src.AnimationFSM import AnimationFSM
from src.AnimatedSprite import AnimatedSprite
from src.LoadResources import SoundEnum
from src.LoadResources import play_sound
from src.LoadResources import ImageEnum
from src.MovingComponent import *
import src.Util

import pygame
from src.Timer import *

BLOCK_SIZE = 32
CONST_CAMERA_PLAYER_OFFSET = 160

CONST_JUMP_VELOCITY = 750
CONST_PLAYER_SPEED = 100
CONST_PLAYER_SPRINT_SPEED = 300
CONST_MAX_ENERGY = 10
CONST_ENERGY_GAIN_RATE = 250
CONST_SPRINT_ENERGY_RATE = 100

from enum import Enum
class PlayerState(Enum):
    GROUND = 0
    JUMPING = 1

class Player:
    def __init__(self, tiles, col, row, level):
        self.size = (BLOCK_SIZE, BLOCK_SIZE)

        self.state = PlayerState.JUMPING

        self.speed = CONST_PLAYER_SPEED
        self.sprint_speed = CONST_PLAYER_SPRINT_SPEED
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

        self.is_sprinting = False

        self.moving_component = MovingComponent(self.sprite, tiles, row, col)
        self.sprite.move(self.moving_component.position)
        self.level = level

        self.life = 10
        self.energy = 10

        self.energy_timer = Timer()

        class Health:
            def __init__(self, health, cooldown_seconds):
                from src.Timer import  Timer
                self.health = health
                self.cooldown_seconds = cooldown_seconds
                self.time_elapsed_since_hit = self.cooldown_seconds
                self.timer = Timer()

            def deal_damage(self, damage):
                t = self.timer.get_time()
                if t > self.cooldown_seconds * 1000:
                    self.health = self.health - damage
                    self.time_elapsed_since_hit = 0
                    self.timer.reset()

                # print("time_elapsed %d" % self.time_elapsed_since_hit)
                # if self.time_elapsed_since_hit >= self.cooldown_seconds:
                #     self.health = self.health - damage
                #     self.time_elapsed_since_hit = 0

            # def update_health(self, deltaTime):
            #     self.time_elapsed_since_hit = self.time_elapsed_since_hit + (deltaTime/1000)

        self.health = Health(100, 3)

        from src.Sprite import Sprite
        self.dot_spr =Sprite(ImageEnum.BLINK_DOT)
        self.shift_is_pressed = False




    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)

        player_rect =self.sprite.sprite_rect()
        x, y = player_rect.topleft
        sprite_rect = self.dot_spr.sprite_rect
        size = abs(sprite_rect.right - sprite_rect.left)

        limit = 10
        for i in range(limit):
            x = x + size
            y = y - size
            self.dot_spr.set_location((x, y))
            self.dot_spr.draw(screen, camera)






    def getrekt(self):
        return pygame.Rect(self.moving_component.position[0],self.moving_component.position[1],self.size[0],self.size[1])

    def print_hello(self):
        print("hello")

    def blink(self):
        mouse_x, mouse_y = self.get_actual_mouse_pos()

        player_x, player_y = self.sprite.sprite_rect().topleft

        cx = int(mouse_x/32)
        cy = int(mouse_y/32)

        d_x = mouse_x - player_x
        d_y = mouse_y - player_y
        print("[blink] displacement %d %d" % (d_x, d_y))

        if self.level.map[cy][cx]:
            print("[blink] wall")
        else:
            self.moving_component.move((d_x, d_y))
            print("[blink] sky")

    def get_actual_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        player_x, player_y = self.sprite.sprite_rect().topleft
        x_origin = player_x - CONST_CAMERA_PLAYER_OFFSET

        mouse_x = x+x_origin
        mouse_y = y

        return mouse_x, mouse_y
        # assert mouse_x != player_x, "x1=x2"
        # assert mouse_y != player_y, "y1=y2"

        # m = (player_y - mouse_y) / (player_x - mouse_x)
        # c = player_y - (m * player_x)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.state==PlayerState.GROUND:
                self.moving_component.velocity = (self.moving_component.velocity[0],self.moving_component.velocity[1] - self.jump_velocity)
                #self.state = PlayerState.JUMPING
                play_sound(SoundEnum.JUMP)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.moving_component.velocity = (0, self.moving_component.velocity[1])

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.blink()




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
                    self.health.deal_damage(10)




    def can_sprint(self):
        if self.energy > 0:
            return True
        else:
            return False

    def update(self, deltatime):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if keys[pygame.K_LSHIFT] and self.can_sprint():
                self.moving_component.velocity = (-self.sprint_speed, self.moving_component.velocity[1])
                self.is_sprinting = True
            else:
                self.moving_component.velocity = (-self.speed, self.moving_component.velocity[1])
                self.is_sprinting = False
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            if keys[pygame.K_LSHIFT] and self.can_sprint():
                self.moving_component.velocity = (self.sprint_speed, self.moving_component.velocity[1])
                self.is_sprinting = True
            else:
                self.moving_component.velocity = (self.speed, self.moving_component.velocity[1])
                self.is_sprinting = False
        else:
            self.moving_component.velocity = (0, self.moving_component.velocity[1])
            self.is_sprinting = False

        self.moving_component.update(deltatime)

        # print(self.moving_component.velocity)
        if not (self.moving_component.in_air):
            self.state = PlayerState.GROUND
            self.update_sprite()
        else:
            self.state = PlayerState.JUMPING
            self.update_sprite()

        t = self.energy_timer.get_time()
        if self.is_sprinting:
            if t > CONST_SPRINT_ENERGY_RATE:
                self.energy_timer.mod_time(CONST_SPRINT_ENERGY_RATE)
                self.energy -= 1
                if self.energy < 0:
                    self.energy = 0
        elif not keys[pygame.K_LSHIFT]:
            if t > CONST_ENERGY_GAIN_RATE:
                self.energy_timer.mod_time(CONST_ENERGY_GAIN_RATE)
                self.energy += 1
                if self.energy >= CONST_MAX_ENERGY:
                    self.energy = CONST_MAX_ENERGY

        self.sprite.update(deltatime)

        # self.health.update_health(deltatime)
        self.handle_enemy_collisions()
