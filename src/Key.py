from src.AnimatedSprite import *
from src.LoadResources import *
from enum import Enum

class KeyEnum(Enum):
    COPPER = 0
    SILVER = 1
    GOLD = 2
    DARK = 3
    MAGIC = 4
    NUM = 5

KeySprites = [ImageEnum.KEY_COPPER,ImageEnum.KEY_SILVER,ImageEnum.KEY_GOLD,ImageEnum.KEY_DARK,ImageEnum.KEY_MAGIC]

class Key:
    def __init__(self, keytype, pos):
        self.key_type = keytype

        frames = 1
        if self.key_type == KeyEnum.SILVER or self.key_type == KeyEnum.GOLD:
            frames = 32

        self.sprite = AnimatedSprite(KeySprites[self.key_type], frames)
        self.sprite.set_location(pos)

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)