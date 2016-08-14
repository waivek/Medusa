from enum import Enum
from src.AnimatedSprite import *

class WeaponEnum(Enum):
    BOW = 0
    GUN = 1

WeaponSprites = [ImageEnum.BOW, ImageEnum.GUN]

class WeaponItem:
    def __init__(self, weapon_type, pos):
        self.sprite = AnimatedSprite(WeaponSprites[weapon_type], 1)
        self.sprite.set_location(pos)
        self.weapon_type = weapon_type

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)