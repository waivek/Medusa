from src.Ammo import *
from src.Projectile import *
from src.Skeleton import *
from src.Vector2i import *

WeaponFunctions = []

class WeaponEquipped:
    def __init__(self, weapon_type, ammo, owner):
        self.weapon_type = weapon_type
        self.ammo = ammo
        self.sprite = AnimatedSprite(WeaponSprites[weapon_type.value],1)
        self.owner = owner

    def use(self, mousepos):
        WeaponFunctions[self.weapon_type.value](self, mousepos)

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)
        self.sprite.set_location(self.owner.moving_component.position)


def init_weapons():

    def passfunc(projectile):
        pass

    def arrowinit(projectile):
        play_sound(SoundEnum.ARROW_SHOOT)
        projectile.moving_component.gravity = 0

    def arrowupd(projectile):
        if projectile.moving_component.velocity == (0,0):
            projectile.owner.level.destroy_entity(projectile)

    def dealdmg(projectile, other):
        print("collision called")
        if isinstance(other, Skeleton):
            other.health -= 1
            projectile.owner.level.destroy_entity(projectile)

    def bow(weapon, target):
        if weapon.ammo > 0:
            weapon.ammo -= 1
            print(target)
            vel = Vector2i(-200, 0)
            rot = math.atan2(-(target[1] - weapon.owner.moving_component.position[1])
                                 ,-(target[0] - weapon.owner.moving_component.position[0]))
            print(rot)
            vel.rotate(rot)
            vel2 = (vel.x,vel.y)
            print(vel2)
            p = Projectile(AmmoSprites[weapon.weapon_type.value], weapon.owner, weapon.owner.moving_component.position, vel2,
                           arrowinit,arrowupd,dealdmg)
            weapon.owner.level.add_entity(p)
    WeaponFunctions.append(bow)

    def gun(weapon, mousepos):
        if weapon.ammo > 0:
            weapon.ammo -= 1
            p = Projectile(AmmoSprites[weapon.weapon_type.value], weapon.owner.moving_component.position, (1000, 0), 10, 0, True, weapon.owner.level)
            weapon.owner.level.add_entity(p)
    WeaponFunctions.append(gun)