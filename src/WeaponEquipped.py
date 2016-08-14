from src.Ammo import *
from src.Projectile import *

class WeaponEquipped:
    def __init__(self, weapon_type, ammo, owner):
        self.weapon_type = weapon_type
        self.ammo = ammo
        self.sprite = AnimatedSprite(WeaponSprites[weapon_type.value],1)
        self.owner = owner

    def use(self):
        if self.ammo > 0:
            self.ammo -= 1
            p = Projectile(AmmoSprites[self.weapon_type.value], self.owner.moving_component.position, (500,0), 10, 0, True, self.owner.level)
            self.owner.level.add_entity(p)

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)
        self.sprite.set_location(self.owner.moving_component.position)