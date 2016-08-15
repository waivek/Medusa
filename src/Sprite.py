import pygame
from src.LoadResources import ImageEnum
from src.LoadResources import gImages
import src.Util
from src.WorldConstants import *

class Sprite:
    def __init__(self, spriteenum):
        self.sprite_enum = spriteenum
        self.sprite = gImages[spriteenum.value]
        self.sprite_rec = self.sprite.get_rect()
        self.bounds = (0,0,32,32)
        self.rotation = 0

    def move(self, displacement):
        self.sprite_rec = self.sprite_rec.move(displacement)

    def set_location(self,pos):
        self.sprite_rec.topleft = pos

    def full_sprite_rect(self):
        return self.sprite_rec

    def sprite_rect(self):
        return pygame.Rect(self.sprite_rec.topleft[0],self.sprite_rec.topleft[1],self.bounds[2],self.bounds[3])

    def get_center(self):
        return (self.sprite_rec.topleft[0] + int(self.bounds[0]/2) , self.sprite_rec.topleft[1] + int(self.bounds[1]/2))

    def draw(self, screen, camera):
        screen_rect = pygame.Rect(camera[0],camera[1],CONST_SCREEN_WIDTH,CONST_SCREEN_HEIGHT)
        if screen_rect.colliderect(self.sprite_rec):
            screen.blit(self.sprite, (self.sprite_rec[0]-camera[0],self.sprite_rec[1]-camera[1],self.sprite_rec[2]-camera[0],
                                  self.sprite_rec[3]-camera[1]), self.bounds)

    def set_rotation(self, angle):
        self.rotation = angle
        self.sprite = pygame.transform.rotate(gImages[self.sprite_enum.value], src.Util.rad2deg(angle))