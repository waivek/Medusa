import pygame
from src.LoadResources import ImageEnum
from src.Sprite import Sprite

class Powerup:
    def __init__(self, pos):
        self.sprite = Sprite(ImageEnum.ITEM_ENERGY)
        self.sprite.set_location(pos)

    def draw(self,screen,camera):
        self.sprite.draw(self, screen, camera)

    def collide(self, player):
        player.jump_velocity *= 2
        player.speed *= 2