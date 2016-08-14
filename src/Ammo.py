from src.WeaponEquipped import *

AmmoSprites = [ImageEnum.AMMO_ARROW, ImageEnum.AMMO_BULLET]

class Ammo:
    def __init__(self, ammo_type, pos):
        self.sprite = AnimatedSprite(AmmoSprites[ammo_type.value], 1)
        self.sprite.set_location(pos)
        self.ammo_type = ammo_type
        self.pos = pos

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)

    def save(self, file):
        file.write(str(self.ammo_type.value))
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
        return (Ammo(WeaponEnum(weapon_type), pos))