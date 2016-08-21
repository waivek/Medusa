import pygame
from src.LoadResources import ImageEnum
from src.LoadResources import gImages
import src.Util
from src.WorldConstants import *
import math

class Sprite:
    def __init__(self, spriteenum):
        self.sprite_enum = spriteenum
        self.sprite = gImages[spriteenum.value]
        self.sprite_rec = self.sprite.get_rect()
        self.bounds = (0,0,32,32)
        self.rotation = 0
        self.is_flipped = False

    def move(self, displacement):
        self.sprite_rec = self.sprite_rec.move(displacement)

    def set_location(self,pos):
        self.sprite_rec.topleft = pos

    def full_sprite_rect(self):
        return self.sprite_rec

    def sprite_rect(self):
        return pygame.Rect(self.sprite_rec.topleft[0]+self.bounds[0],self.sprite_rec.topleft[1]+self.bounds[1],self.bounds[2],self.bounds[3])

    def get_center(self):
        return (self.sprite_rec.topleft[0]+self.bounds[0] + int(self.bounds[2]/2) , self.sprite_rec.topleft[1]+self.bounds[1] + int(self.bounds[3]/2))

    def draw(self, screen, camera):
        screen_rect = pygame.Rect(camera[0],camera[1],CONST_SCREEN_WIDTH,CONST_SCREEN_HEIGHT)
        if screen_rect.colliderect(self.sprite_rec):
            screen.blit(self.sprite, pygame.Rect(self.sprite_rec[0]-camera[0],self.sprite_rec[1]-camera[1],self.sprite_rec[2]-camera[0],
                                  self.sprite_rec[3]-camera[1]), pygame.Rect(self.bounds))

    def set_rotation_cropped(self, angle):
        self.set_rotation_cropped_degrees(math.degrees(angle))

    def set_rotation_cropped_degrees(self, angle):
        self.rotation = angle
        self.sprite = pygame.transform.rotate(gImages[self.sprite_enum.value], angle)
        if self.is_flipped:
            self.is_flipped = False
            self.flip()

    def set_rotation(self, angle):
        self.set_rotation_cropped_degrees(angle)

    def set_rotation_degrees(self, angle):
        self.rotation = angle
        self.sprite = pygame.transform.rotate(gImages[self.sprite_enum.value], angle)
        self.sprite_rec = self.sprite.get_rect(center=self.sprite_rec.center)
        self.bounds = (0, 0, self.sprite_rec[2], self.sprite_rec[3])

    def rotate_around_point(self, angle, point):
        surface = pygame.Surface((2 * point[0], 2 * point[1]), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        surface.blit(self.sprite, (0, 0, 2 * point[0], 2 * point[1]), self.bounds)
        self.sprite = pygame.transform.rotate(surface, angle)
        self.sprite_rec = self.sprite.get_rect(center=self.sprite_rec.center)
        self.bounds = (0,0,self.sprite_rec[2],self.sprite_rec[3])

        if self.is_flipped:
            self.is_flipped = False
            self.flip()

    def flip(self):
        self.is_flipped = not self.is_flipped
        self.sprite = pygame.transform.flip(self.sprite, True, False)

    def set_flipped(self, value):
        if value!=self.is_flipped:
            self.flip()

    def get_mask(self):
        return pygame.mask.from_surface(self.sprite)