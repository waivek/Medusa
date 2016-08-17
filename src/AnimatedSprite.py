import pygame
from src.LoadResources import *
from src.Timer import *
import math

class AnimatedSprite:
    def __init__(self, img_id, frames):
        self.image_id = img_id
        self.frequency = 100
        self.bounds = (32,32)
        self.timer = Timer()
        self.current_frame = 0
        self.max_frames = frames
        self.sprite_rec = gImages[self.image_id.value].get_rect()
        self.rotation = 0

    def full_sprite_rect(self):
        return self.sprite_rec

    def sprite_rect(self):
        return pygame.Rect(self.sprite_rec.topleft[0],self.sprite_rec.topleft[1],self.bounds[0],self.bounds[1])

    def get_center(self):
        return (self.sprite_rec.topleft[0] + int(self.bounds[0]/2) , self.sprite_rec.topleft[1] + int(self.bounds[1]/2))

    def next_frame(self):
        self.current_frame += 1
        self.current_frame %= self.max_frames

    def reset(self):
        self.current_frame = 0
        self.timer.reset()

    def update(self, deltatime):
        time = self.timer.get_time()
        if time >= self.frequency:
            self.timer.mod_time(self.frequency)
            self.next_frame()

    def draw(self, screen, camera):
        rect = pygame.Rect((self.current_frame*self.bounds[0],0),self.bounds)

        spr_pos = (self.sprite_rec[0]-camera[0],self.sprite_rec[1]-camera[1],self.sprite_rec[2]-camera[0],
                                  self.sprite_rec[3]-camera[1])
        screen.blit(gImages[self.image_id.value], spr_pos, rect)

    def move(self, displacement):
        self.sprite_rec = self.sprite_rec.move(displacement)

    def set_location(self, pos):
        self.sprite_rec.topleft = pos

    def set_rotation(self, angle):
        self.rotation = angle
        self.sprite = pygame.transform.rotate(gImages[self.image_id.value], math.degrees(angle))

    def get_mask(self):
        m = pygame.Mask((32,32))
        m.fill()
        return m

    def get_frame(self):
        return self.current_frame