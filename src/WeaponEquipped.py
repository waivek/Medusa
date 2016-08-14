from src.WeaponItem import *

class WeaponEquipped:
    def __init__(self, weapon_type, ammo, owner):
        self.weapon_type = weapon_type
        self.ammo = ammo
        self.sprite = AnimatedSprite(WeaponSprites[weapon_type],1)
        self.owner = owner

    def use(self):
        if self.ammo > 0:
            self.ammo -= 1

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)
        self.sprite.set_location(self.owner.moving_component.position)