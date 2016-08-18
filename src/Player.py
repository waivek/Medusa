from src.Skeleton import *
from src.Powerup import *
from src.Lock import *
from src.WeaponEquipped import *
import src.Util
from src.BlinkComponent import *

import pygame
# import pygame
from src.Timer import *

from enum import Enum
class PlayerState(Enum):
    GROUND = 0
    JUMPING = 1

class PlayerAnimState(Enum):
    WALK_LEFT = 0
    WALK_RIGHT = 1
    JUMP_LEFT = 2
    JUMP_RIGHT = 3
    LEFT = 4
    RIGHT = 5
    STAB_LEFT = 6
    STAB_RIGHT = 7

class Player:
    def __init__(self, pos, level):
        self.level = level

        self.size = (BLOCK_SIZE, BLOCK_SIZE)

        self.state = PlayerState.JUMPING

        self.speed = CONST_PLAYER_SPEED
        self.sprint_speed = CONST_PLAYER_SPRINT_SPEED
        self.jump_velocity = CONST_JUMP_VELOCITY
        self.energy_regain_rate = CONST_ENERGY_GAIN_RATE
        self.sprint_energy_rate = CONST_SPRINT_ENERGY_RATE

        self.facing = Facing.LEFT
        self.is_attacking = False

        self.sprite = AnimationFSM()
        spr0 = AnimatedSprite(ImageEnum.PLAYER1_LEFT, 8)
        spr1 = AnimatedSprite(ImageEnum.PLAYER1_RIGHT, 8)
        spr2 = AnimatedSprite(ImageEnum.PLAYER1_JUMPLEFT, 1)
        spr3 = AnimatedSprite(ImageEnum.PLAYER1_JUMPRIGHT, 1)
        spr4 = AnimatedSprite(ImageEnum.PLAYER1_LEFT, 1)
        spr5 = AnimatedSprite(ImageEnum.PLAYER1_RIGHT, 1)
        spr6 = AnimatedSprite(ImageEnum.PLAYER1_STABLEFT, 4)
        spr7 = AnimatedSprite(ImageEnum.PLAYER1_STABRIGHT, 4)
        self.sprite.add_sprite(spr0)
        self.sprite.add_sprite(spr1)
        self.sprite.add_sprite(spr2)
        self.sprite.add_sprite(spr3)
        self.sprite.add_sprite(spr4)
        self.sprite.add_sprite(spr5)
        self.sprite.add_sprite(spr6)
        self.sprite.add_sprite(spr7)

        self.sprite.set_state(PlayerAnimState.JUMP_LEFT)

        self.is_sprinting = False

        self.moving_component = MovingComponent(self, self.level)
        self.moving_component.move(pos)
        self.moving_component.on_collision = Player.on_collision

        self.equip_component = EquipComponent(self, self.level)
        self.equip_component.print_attach_points()

        self.energy = 10
        self.energy_timer = Timer()

        self.valid_blink_points = []

        self.health = Health(10, 1)

        self.buffs = []

        from src.Sprite import Sprite
        self.dot_spr =Sprite(ImageEnum.BLINK_DOT)
        self.dot_spr.bounds = (0, 0, 4, 4)
        self.can_blink = False

        self.keys = []
        for i in range(KeyEnum.NUM.value):
            self.keys.append(0)

        self.equipped_weapon = -1
        self.weapon = []
        for i in range(WeaponEnum.NUM.value):
            self.weapon.append(None)
        self.blink_component = BlinkComponent(player=self)

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)
        if self.equipped_weapon is not -1:
            self.weapon[self.equipped_weapon].draw(screen, camera)
        self.blink_component.draw(screen, camera)


    def handle_event(self, event):
        self.blink_component.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.state==PlayerState.GROUND:
                self.moving_component.velocity = (self.moving_component.velocity[0],self.moving_component.velocity[1] - self.jump_velocity)
                #self.state = PlayerState.JUMPING
                play_sound(SoundEnum.JUMP)

            elif event.key == pygame.K_e:
                i = self.equipped_weapon + 1
                while i < WeaponEnum.NUM.value:
                    if self.weapon[i] is not None:
                        self.equipped_weapon = i
                        break
                    i+=1

            elif event.key == pygame.K_q:
                i = self.equipped_weapon - 1
                while i >= 0:
                    if self.weapon[i] is not None:
                        self.equipped_weapon = i
                        break
                    i-=1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.equipped_weapon != -1:
                mpos = pygame.mouse.get_pos()
                target = (mpos[0]+self.level.camera_pos[0],mpos[1]+self.level.camera_pos[1])
                self.weapon[self.equipped_weapon].use(target)
                self.is_attacking = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.moving_component.velocity = (0, self.moving_component.velocity[1])

    def update_sprite(self):
        if self.is_attacking:
           if self.sprite.get_loop() > 0:
               self.is_attacking = False

        if not self.is_attacking:
            if self.state == PlayerState.JUMPING:
                if self.moving_component.velocity[0] >= 0:
                    self.sprite.set_state(PlayerAnimState.JUMP_RIGHT)
                    self.facing = Facing.RIGHT
                else:
                    self.sprite.set_state(PlayerAnimState.JUMP_LEFT)
                    self.facing = Facing.LEFT
            else:
                if self.moving_component.velocity[0] > 0:
                    self.sprite.set_state(PlayerAnimState.WALK_RIGHT)
                    self.facing = Facing.RIGHT
                elif self.moving_component.velocity[0] < 0:
                    self.sprite.set_state(PlayerAnimState.WALK_LEFT)
                    self.facing = Facing.LEFT
                else:
                    if self.facing == Facing.RIGHT:
                        self.sprite.set_state(PlayerAnimState.RIGHT)
                    if self.facing == Facing.LEFT:
                        self.sprite.set_state(PlayerAnimState.LEFT)


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
        #parse buffs
        self.update_buffs(deltatime)
        
        #detect input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            if keys[SPRINT_KEY] and self.can_sprint():
                self.moving_component.velocity = (-self.sprint_speed, self.moving_component.velocity[1])
                self.is_sprinting = True
            else:
                self.moving_component.velocity = (-self.speed, self.moving_component.velocity[1])
                self.is_sprinting = False
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            if keys[SPRINT_KEY] and self.can_sprint():
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
        elif not keys[SPRINT_KEY]:
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

        #self.moving_component.push_out_colliders(self.level.colliders)

        if self.equipped_weapon is not -1:
            self.weapon[self.equipped_weapon].update(deltatime)

    def save(self, file):
        file.write(str(self.moving_component.position[0]))
        file.write('\n')
        file.write(str(self.moving_component.position[1]))
        file.write('\n')

    @staticmethod
    def load(file, level):
        posx = int(file.readline())
        posy = int(file.readline())
        pos = (posx, posy)
        return (Player(pos, level))

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

        if isinstance(other, Ammo):
            if self.weapon[other.ammo_type.value] is not None:
                self.weapon[other.ammo_type.value].ammo += 5
                self.level.destroy_entity(other)

        if isinstance(other, WeaponItem):
            if self.weapon[other.weapon_type.value] is None:
                self.weapon[other.weapon_type.value] = WeaponEquipped(other.weapon_type,5,self)
                if self.equipped_weapon == -1:
                    self.equipped_weapon = other.weapon_type.value
                    self.equip_component.equip_right(self.weapon[other.weapon_type.value])

            else:
                self.weapon[other.weapon_type.value].ammo += 5
            self.level.destroy_entity(other)
