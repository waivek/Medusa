from src.AnimatedSprite import *
from src.LoadResources import *
from enum import Enum

class KeyEnum(Enum):
    COPPER = 0
    SILVER = 1
    GOLD = 2
    DARK = 3
    MAGIC = 4
    WOOD = 5
    BLUE = 6
    NUM = 7

KeySprites = [ImageEnum.KEY_COPPER,ImageEnum.KEY_SILVER,ImageEnum.KEY_GOLD,ImageEnum.KEY_DARK,ImageEnum.KEY_MAGIC
    ,ImageEnum.KEY_WOOD,ImageEnum.KEY_BLUE]

class Key:
    def __init__(self, keytype, pos):
        self.key_type = keytype
        self.pos = pos
        frames = 1
        if self.key_type == KeyEnum.SILVER or self.key_type == KeyEnum.GOLD:
            frames = 32

        self.sprite = AnimatedSprite(KeySprites[self.key_type.value], frames)
        self.sprite.set_location(pos)

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)

    def save(self, file):
        file.write(str(self.key_type.value))
        file.write('\n')
        file.write(str(self.pos[0]))
        file.write('\n')
        file.write(str(self.pos[1]))
        file.write('\n')

    @staticmethod
    def load(file, level):
        key_type = int(file.readline())
        posx = int(file.readline())
        posy = int(file.readline())
        pos = (posx, posy)
        return (Key(KeyEnum(key_type),pos))