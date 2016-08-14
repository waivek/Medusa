from src.WeaponItem import *

AmmoSprites = [ImageEnum.ARROW, ImageEnum.BULLET]

class Ammo:
    def __init__(self, weapon_type, pos):
        self.sprite = AnimatedSprite(AmmoSprites[weapon_type], 1)
        self.sprite.set_location(pos)
        self.weapon_type = weapon_type

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)