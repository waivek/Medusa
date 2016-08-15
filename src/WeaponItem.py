from enum import Enum
from src.AnimatedSprite import *

class WeaponEnum(Enum):
    BOW = 0
    GUN = 1
    NUM = 2

WeaponSprites = [ImageEnum.WEAPON_BOW, ImageEnum.WEAPON_GUN]

class WeaponItem:
    def __init__(self, weapon_type, pos):
        self.sprite = AnimatedSprite(WeaponSprites[weapon_type.value], 1)
        self.sprite.set_location(pos)
        self.weapon_type = weapon_type
        self.pos = pos

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)

    def save(self, file):
        file.write(str(self.weapon_type.value))
        file.write('\n')
        file.write(str(self.pos[0]))
        file.write('\n')
        file.write(str(self.pos[1]))
        file.write('\n')

    @staticmethod
    def load(file, level):
        weapon_type = int(file.readline())
        posx = int(file.readline())
        posy = int(file.readline())
        pos = (posx, posy)
        return (WeaponItem(WeaponEnum(weapon_type), pos))