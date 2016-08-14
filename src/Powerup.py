import pygame
from src.LoadResources import *
from src.AnimatedSprite import *

class Powerup:
    def __init__(self, spriteenum, frames, pos):
        self.sprite = AnimatedSprite(spriteenum, frames)
        self.sprite.set_location(pos)
        self.buff = None

    def draw(self,screen,camera):
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        self.sprite.update(deltatime)