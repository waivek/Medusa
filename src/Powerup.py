import pygame
from src.LoadResources import ImageEnum
from src.Sprite import Sprite

class Powerup:
    def __init__(self, spriteenum, pos):
        self.sprite = Sprite(spriteenum)
        self.sprite.set_location(pos)

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)