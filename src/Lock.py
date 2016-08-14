from src.AnimatedSprite import *
from src.LoadResources import *
from src.Key import *
from enum import Enum

LockSprites = [ImageEnum.LOCK_COPPER, ImageEnum.LOCK_SILVER, ImageEnum.LOCK_GOLD, ImageEnum.LOCK_DARK, ImageEnum.LOCK_MAGIC]


class Lock:
    def __init__(self, locktype, pos):
        self.lock_type = locktype
        self.pos = pos
        frames = 1
        if self.lock_type == KeyEnum.SILVER or self.lock_type == KeyEnum.GOLD:
            frames = 32

        self.sprite = AnimatedSprite(LockSprites[self.lock_type.value], frames)
        self.sprite.set_location(pos)

    def draw(self, screen, camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)

    def save(self, file):
        file.write(str(self.lock_type.value))
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
        pos = (posx,posy)
        return (Lock(KeyEnum(key_type),pos))