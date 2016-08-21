from src.MovingComponent import *
from src.EquipComponent import *
from src.Health import *
from src.SkeletonAI import SkeletonAI
import pygame

from enum import Enum

class SkeletonState(Enum):
    GROUND = 0
    IN_AIR = 1

class Skeleton:
    def __init__(self, pos, level):
        self.sprite = AnimationFSM()
        self.level = level
        #spr0 = AnimatedSprite(ImageEnum.SKELETON_STANDING, 1)
        spr1 = AnimatedSprite(ImageEnum.SKELETON_WALKLEFT, 4)
        spr2 = AnimatedSprite(ImageEnum.SKELETON_WALKRIGHT, 4)
        spr3 = AnimatedSprite(ImageEnum.SKELETON_STABLEFT, 4)
        spr4 = AnimatedSprite(ImageEnum.SKELETON_STABRIGHT, 4)
        #self.sprite.add_sprite(spr0)
        self.sprite.add_sprite(spr1)
        self.sprite.add_sprite(spr2)
        self.sprite.add_sprite(spr3)
        self.sprite.add_sprite(spr4)
        self.sprite.state = 0
        self.state = SkeletonState.IN_AIR
        self.moving_component = MovingComponent(self, self.level)
        self.moving_component.update_position(pos)
        #self.enemy_movement_component = EnemyMovementComponent(self, self.level)
        self.moving_component.on_collision = Skeleton.on_collision
        self.health = 1

        self.equip_component = EquipComponent(self, self.level)
        self.weapon = WeaponEquipped(WeaponEnum.SHORTSWORD,5,self)
        self.equip_component.equip_right(self.weapon)

        self.ai_component = SkeletonAI(self)

        self.facing = Facing.LEFT

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)
        self.equip_component.draw_right(screen, camera)

    def getrekt(self):
        return pygame.Rect(self.moving_component.position[0],self.moving_component.position[1],self.moving_component.size[0],self.moving_component.size[1])

    def set_to_ground(self):
        self.state = SkeletonState.GROUND

    def update_sprite(self):
        if self.equip_component.is_attacking:
            if self.sprite.get_loop()>0:
                self.equip_component.is_attacking = False

        if not self.equip_component.is_attacking:
            if self.moving_component.velocity[0] < 0:
                self.sprite.set_state(0)
                self.facing = Facing.LEFT
            elif self.moving_component.velocity[0] > 0:
                self.sprite.set_state(1)
                self.facing = Facing.RIGHT

    def attack(self):
        self.equip_component.is_attacking = True
        self.weapon.is_attacking = True
        if self.facing == Facing.LEFT:
            self.sprite.set_state(2)
        else:
            self.sprite.set_state(3)

    def update(self, deltaTime):
        if self.health <= 0:
            self.level.destroy_entity(self)

        self.moving_component.update(deltaTime)
        self.weapon.update(deltaTime)
        self.ai_component.update(deltaTime)
        self.sprite.update(deltaTime)
        self.update_sprite()

    def move_direction(self, direction):
        if direction==Facing.LEFT:
            self.moving_component.velocity = (-100, self.moving_component.velocity[1])
        else:
            self.moving_component.velocity = (100, self.moving_component.velocity[1])

    def stand_still(self):
        self.moving_component.velocity = (0, self.moving_component.velocity[1])

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

    @staticmethod
    def on_collision(this, other):
        #print("collision with")
        #print(type(other))

        if isinstance(other, BlockCollision):
            pass
            # if other.x*BLOCK_SIZE == this.sprite.sprite_rect().topleft[1]:
            #     #print("%d %d %d" % (other.x*32,other.y*32,this.sprite.sprite_rect().topleft[1]))
            #     if other.y * BLOCK_SIZE > this.sprite.sprite_rect().topleft[0]:
            #         this.moving_component.velocity = (-100, this.moving_component.velocity[1])
            #     else:
            #         this.moving_component.velocity = (100, this.moving_component.velocity[1])
        else:
            if other.sprite.sprite_rect().topleft[0] > this.sprite.sprite_rect().topleft[0]:
                this.moving_component.velocity = (-100,this.moving_component.velocity[1])
            else:
                this.moving_component.velocity = (100, this.moving_component.velocity[1])
        #print(this.moving_component.velocity)