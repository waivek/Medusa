from src.Skeleton import *
from src.Powerup import *
from src.Lock import *
# import pygame
from src.Timer import *


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.m = (y2 - y1) / (x2 - x1)
        self.c = y1 - (self.m * x1)

    def get_y(self, x1):
        y1 = (self.m * x1) + self.c
        return y1

    def get_x(self, y1):
        x1 = (y1 - self.c) / self.m
        return x1

class Blink_Component:
    def __init__(self, player):
        from src.Sprite import Sprite
        self.valid_blink_points = []
        self.dot_spr =Sprite(ImageEnum.BLINK_DOT)
        self.dot_spr.bounds = (0, 0, 4, 4)
        self.can_blink = False
        self.player = player

        self.blink_frames = 3
        self.is_blinking = False
        self.frame_displacement = (None, None)
        self.frames_passed = None
        self.old_offset = None

    def get_actual_mouse_pos(self):
        from src.WorldConstants import CONST_CAMERA_PLAYER_OFFSET_X, CONST_CAMERA_PLAYER_OFFSET_Y
        import pygame
        x, y = pygame.mouse.get_pos()
        player_x, player_y = self.player.sprite.sprite_rect().topleft
        x_origin = player_x - CONST_CAMERA_PLAYER_OFFSET_X
        # x_origin = 0
        # y_origin = player_y - CONST_CAMERA_PLAYER_OFFSET_Y
        y_origin = 0

        mouse_x = x+x_origin
        mouse_y = y+y_origin

        return mouse_x, mouse_y

    def fill_valid_blink_points(self):
        player_x, player_y = self.player.sprite.sprite_rect().center
        mouse_x, mouse_y = self.get_actual_mouse_pos()
        if mouse_x == player_x:
            mouse_x = mouse_x + 1
        m = (player_y - mouse_y) / (player_x - mouse_x)
        c = player_y - (m * player_x)

        self.valid_blink_points = []

        step = 0

        if player_x <= mouse_x:
            step = 1
        elif mouse_x < player_x:
            step = -1

        for x in range(player_x, mouse_x, step):
            y = m*x + c
            if self.pos_is_tile(x, y):
                break
            self.valid_blink_points.append((x, y))

    def draw(self, screen, camera):
        if self.can_blink:
            self.fill_valid_blink_points()
            for x, y in self.valid_blink_points:
                self.dot_spr.set_location((x, y))
                self.dot_spr.draw(screen, camera)

    def blink(self):
        # if not self.is_blinking:
        # self.is_blinking = True
        player_x, player_y = self.player.sprite.sprite_rect().center
        valid_x, valid_y = self.valid_blink_points[-1]

        damper_x = 0
        damper_y= 0

        d_x = (valid_x - player_x) - damper_x
        d_y = (valid_y - player_y) - damper_y

        # self.frame_displacement = (d_x / self.blink_frames,
        #                            d_y / self.blink_frames)
        # self.frames_passed = 0

        self.player.moving_component.move((d_x, d_y))
        # self.player.moving_component.move(self.frame_displacement)
        # self.frames_passed = self.frames_passed + 1

        # elif  self.is_blinking:
        #     if self.frames_passed < self.blink_frames:
        #         self.player.moving_component.move(self.frame_displacement)
        #         self.frames_passed = self.frames_passed + 1
        #     elif self.frames_passed >= self.blink_frames:
        #         self.is_blinking = False

    def handle_event(self, event):
        from src.WorldConstants import BLINK_KEY
        if event.type == pygame.KEYDOWN:
            if event.key == BLINK_KEY:
                self.can_blink = True

        elif event.type == pygame.KEYUP:
            if event.key == BLINK_KEY:
                self.can_blink = False

        if event.type == pygame.MOUSEBUTTONDOWN and self.can_blink:
            self.is_blinking = True

    def pos_is_tile(self, x, y):
        i = int(x/32)
        j = int(y/32)

        if self.player.level.map[j][i]:
            return True
        else:
            return False

    def update(self, deltaTime):
        if self.is_blinking:
            is_first_blink_frame = self.frames_passed == None
            if is_first_blink_frame:

                self.old_offset = CONST_CAMERA_PLAYER_OFFSET_X

                self.frames_passed = 0

                player_x, player_y = self.player.sprite.sprite_rect().center
                valid_x, valid_y = self.valid_blink_points[-1]
                d_x = (valid_x - player_x)
                d_y = (valid_y - player_y)

                self.frame_displacement = (d_x / self.blink_frames,
                                           d_y / self.blink_frames)
                self.player.moving_component.move(self.frame_displacement)

                self.frames_passed = self.frames_passed + 1
            elif not is_first_blink_frame:
                if self.frames_passed < self.blink_frames:
                    self.player.moving_component.move(self.frame_displacement)
                    self.frames_passed = self.frames_passed + 1
                elif self.frames_passed >= self.blink_frames:
                    self.is_blinking = False
                    self.frames_passed = None
                    self.frame_displacement = (None, None)

            # self.player.moving_component.move((d_x, d_y))
            # self.is_blinking = False

from enum import Enum
class PlayerState(Enum):
    GROUND = 0
    JUMPING = 1

class Player:
    def __init__(self, pos, level):
        self.size = (BLOCK_SIZE, BLOCK_SIZE)

        self.state = PlayerState.JUMPING

        self.speed = CONST_PLAYER_SPEED
        self.sprint_speed = CONST_PLAYER_SPRINT_SPEED
        self.jump_velocity = CONST_JUMP_VELOCITY
        self.energy_regain_rate = CONST_ENERGY_GAIN_RATE
        self.sprint_energy_rate = CONST_SPRINT_ENERGY_RATE

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

        self.moving_component = MovingComponent(self.sprite, level.map, level.row, level.col)
        self.moving_component.move(pos)
        self.level = level

        self.energy = 10
        self.energy_timer = Timer()

        self.valid_blink_points = []

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

        self.health = Health(10, 1)

        self.buffs = []

        from src.Sprite import Sprite
        self.dot_spr =Sprite(ImageEnum.BLINK_DOT)
        self.dot_spr.bounds = (0, 0, 4, 4)
        self.can_blink = False

        self.keys = []
        for i in range(KeyEnum.NUM.value):
            self.keys.append(0)

        self.blink_component = Blink_Component(player=self)

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)
        self.blink_component.draw(screen, camera)


    def handle_event(self, event):
        self.blink_component.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.state==PlayerState.GROUND:
                self.moving_component.velocity = (self.moving_component.velocity[0],self.moving_component.velocity[1] - self.jump_velocity)
                play_sound(SoundEnum.JUMP)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.moving_component.velocity = (0, self.moving_component.velocity[1])

    def update_sprite(self):
        if self.state == PlayerState.JUMPING:
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

    def on_collision(self, other):
        if isinstance(other, Skeleton):
            self.health.deal_damage(1)

        if isinstance(other, Powerup):
            other.buff.start()
            self.buffs.append(other.buff)
            self.level.destroy_entity(other)
            play_sound(SoundEnum.POWERUP)

        if isinstance(other, Key):
            self.keys[other.key_type.value] += 1
            self.level.destroy_entity(other)

        if isinstance(other, Lock):
            if self.keys[other.lock_type.value] > 0:
                self.keys[other.lock_type.value] -= 1
                self.level.destroy_entity(other)
                play_sound(SoundEnum.UNLOCK)

    def handle_collisions(self):
        entities = self.level.entities
        def lies_between(x, a, b):
            return a <= x <= b

        for other in entities:
            #assert(isinstance(other, Skeleton))
            player_rect =self.sprite.sprite_rect()
            assert(isinstance(player_rect, pygame.Rect))

            other_rect = other.sprite.sprite_rect()
            assert(isinstance(other_rect, pygame.Rect))

            collision = {}
            collision["right"] = lies_between(other_rect.left, player_rect.left, player_rect.right)
            collision["left"] = lies_between(other_rect.right, player_rect.left, player_rect.right)
            if collision["left"] or collision["right"]:
                collision["up"] = lies_between(other_rect.bottom, player_rect.top, player_rect.bottom)
                collision["down"] = lies_between(other_rect.top, player_rect.top, player_rect.bottom)
                if collision["down"] or collision["up"]:
                    self.on_collision(other)

    def update_buffs(self, deltatime):
        self.speed = CONST_PLAYER_SPEED
        self.sprint_speed = CONST_PLAYER_SPRINT_SPEED
        self.jump_velocity = CONST_JUMP_VELOCITY
        self.energy_regain_rate = CONST_ENERGY_GAIN_RATE
        self.sprint_energy_rate = CONST_SPRINT_ENERGY_RATE
        self.moving_component.gravity = CONST_GRAVITY
        self.moving_component.bounciness = 0

        for buff in self.buffs:
            buff.update(deltatime)
            if buff.is_expired:
                self.buffs.remove(buff)
            else:
                buff.call_func(self, buff)

    def can_sprint(self):
        if self.energy > 0:
            return True
        else:
            return False

    def update(self, deltatime):
        self.blink_component.update(deltatime)
        #parse buffs
        self.update_buffs(deltatime)

        #detect input
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

        #set sprite
        if not self.moving_component.in_air:
            self.state = PlayerState.GROUND
            self.update_sprite()
        else:
            self.state = PlayerState.JUMPING
            self.update_sprite()

        #sprinting
        t = self.energy_timer.get_time()
        if self.is_sprinting:
            if t > self.sprint_energy_rate:
                self.energy_timer.mod_time(self.sprint_energy_rate)
                self.energy -= 1
                if self.energy < 0:
                    self.energy = 0
        elif not keys[pygame.K_LSHIFT]:
            if t > self.energy_regain_rate:
                self.energy_timer.mod_time(self.energy_regain_rate)
                self.energy += 1
                if self.energy >= CONST_MAX_ENERGY:
                    self.energy = CONST_MAX_ENERGY

        self.sprite.update(deltatime)

        if self.health.health > CONST_MAX_HEALTH:
            self.health.health = CONST_MAX_HEALTH

        #handle collisions
        self.handle_collisions()

        colliders = []
        for ent in self.level.entities:
            if isinstance(ent, Lock) or isinstance(ent, Skeleton):
                colliders.append(ent)

        self.moving_component.push_out_colliders(colliders)
