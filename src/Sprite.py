import pygame
from src.LoadResources import ImageEnum
from src.LoadResources import gImages

class Sprite:
    def __init__(self, spriteenum):
        self.sprite = gImages[spriteenum.value]
        self.sprite_rect = self.sprite.get_rect()

    def move(self, displacement):
        self.sprite_rect = self.sprite_rect.move(displacement)

    def set_location(self,pos):
        self.sprite_rect.topleft = pos

    def draw(self, screen, camera):
        screen.blit(self.sprite, (self.sprite_rect[0]-camera[0],self.sprite_rect[1]-camera[1],self.sprite_rect[2]-camera[0],
                                  self.sprite_rect[3]-camera[1]))
