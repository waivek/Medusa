from src.Ammo import *
from src.Projectile import *
from src.Skeleton import *

WeaponFunctions = []

class WeaponEquipped:
    def __init__(self, weapon_type, ammo, owner):
        self.weapon_type = weapon_type
        self.ammo = ammo
        self.sprite = Sprite(WeaponSprites[weapon_type.value])
        self.owner = owner

    def use(self, mousepos):
        WeaponFunctions[self.weapon_type.value](self, mousepos)

    def draw(self,screen,camera):
        from src.Player import PlayerAnimState
        self.sprite.set_rotation_degrees(90 - (self.owner.sprite.sprites[self.owner.sprite.state].current_frame % 4)*30)
        if self.owner.sprite.state == PlayerAnimState.WALK_RIGHT.value or self.owner.sprite.state == PlayerAnimState.RIGHT.value \
            or self.owner.sprite.state == PlayerAnimState.JUMP_RIGHT.value:
            self.sprite.set_flipped(True)
        else:
            self.sprite.set_flipped(False)
        self.sprite.draw(screen, camera)
        print(self.sprite.is_flipped)

    def update(self, deltatime):
        #self.sprite.update(deltatime)
        self.sprite.set_location(self.owner.moving_component.position)


def init_weapons():

    def passfunc(projectile):
        pass

    def arrowinit(projectile):
        play_sound(SoundEnum.ARROW_SHOOT)
        projectile.moving_component.gravity = 0
        projectile.moving_component.collision_bounds = pygame.Rect(1,11,30,11)

    def arrowupd(projectile):
        if projectile.moving_component.velocity == (0,0):
            projectile.owner.level.destroy_entity(projectile)

    def dealdmg(projectile, other):
        print("collision called")
        if isinstance(other, Skeleton):
            other.health -= 1
            projectile.owner.level.destroy_entity(projectile)
        else:
            projectile.owner.level.destroy_entity(projectile)

    def bow(weapon, target):
        if weapon.ammo > 0:
            weapon.ammo -= 1
            vel = pygame.math.Vector2(500, 0)
            rot = math.atan2((target[1] - weapon.owner.moving_component.position[1])-16
                                 ,(target[0] - weapon.owner.moving_component.position[0])-16)
            vel = vel.rotate(math.degrees(rot))
            vel2 = (vel.x,vel.y)
            p = Projectile(AmmoSprites[weapon.weapon_type.value], weapon.owner, weapon.owner.moving_component.position, vel2,
                           arrowinit,arrowupd,dealdmg)
            weapon.owner.level.add_entity(p)
    WeaponFunctions.append(bow)

    def gun(weapon, target):
        if weapon.ammo > 0:
            weapon.ammo -= 1
            p = Projectile(AmmoSprites[weapon.weapon_type.value], weapon.owner.moving_component.position, (1000, 0), 10, 0, True, weapon.owner.level)
            weapon.owner.level.add_entity(p)
    WeaponFunctions.append(gun)