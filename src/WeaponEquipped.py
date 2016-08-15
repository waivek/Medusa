from src.Ammo import *
from src.Projectile import *
from src.Skeleton import *

WeaponFunctions = []

class WeaponEquipped:
    def __init__(self, weapon_type, ammo, owner):
        self.weapon_type = weapon_type
        self.ammo = ammo
        self.sprite = AnimatedSprite(WeaponSprites[weapon_type.value],1)
        self.owner = owner

    def use(self):
        WeaponFunctions[self.weapon_type.value](self)

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)
        self.sprite.set_location(self.owner.moving_component.position)


def init_weapons():

    def passfunc(projectile):
        pass

    def dealdmg(projectile, other):
        if isinstance(other, Skeleton):
            other.health -= 1
            projectile.owner.level.destroy_entity(projectile)

    def bow(weapon):
        if weapon.ammo > 0:
            weapon.ammo -= 1
            p = Projectile(AmmoSprites[weapon.weapon_type.value], weapon.owner, weapon.owner.moving_component.position, (500, 0),
                           passfunc,passfunc,dealdmg)
            weapon.owner.level.add_entity(p)
    WeaponFunctions.append(bow)

    def gun(weapon):
        if weapon.ammo > 0:
            weapon.ammo -= 1
            p = Projectile(AmmoSprites[weapon.weapon_type.value], weapon.owner.moving_component.position, (1000, 0), 10, 0, True, weapon.owner.level)
            weapon.owner.level.add_entity(p)
    WeaponFunctions.append(gun)