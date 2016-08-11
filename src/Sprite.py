import pygame
from src.LoadResources import ImageEnum
from src.LoadResources import gImages

class Sprite:
    def __init__(self, spriteenum):
        self.sprite = gImages[spriteenum.value]
        self.sprite_rec = self.sprite.get_rect()
        self.bounds = (0,0,32,32)

    def move(self, displacement):
        self.sprite_rec = self.sprite_rec.move(displacement)

    def set_location(self,pos):
        self.sprite_rec.topleft = pos

    def full_sprite_rect(self):
        return self.sprite_rec

    def sprite_rect(self):
        return pygame.Rect(self.sprite_rec.topleft[0],self.sprite_rec.topleft[1],self.bounds[0],self.bounds[1])

    def draw(self, screen, camera):
        screen.blit(self.sprite, (self.sprite_rec[0]-camera[0],self.sprite_rec[1]-camera[1],self.sprite_rec[2]-camera[0],
                                  self.sprite_rec[3]-camera[1]), self.bounds)
