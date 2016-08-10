import pygame
from src.LoadResources import gImages
from src.LoadResources import ImageEnum
from src.Timer import Timer

class AnimatedSprite:
    def __init__(self, img_id, frames):
        self.image_id = img_id
        self.frequency = 100
        self.bounds = (32,32)
        self.timer = Timer()
        self.current_frame = 0
        self.max_frames = frames
        self.sprite_rect = gImages[self.image_id.value].get_rect()

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

        spr_pos = (self.sprite_rect[0]-camera[0],self.sprite_rect[1]-camera[1],self.sprite_rect[2]-camera[0],
                                  self.sprite_rect[3]-camera[1])
        screen.blit(gImages[self.image_id.value], spr_pos, rect)

    def get_pos_rect(self):
        return pygame.Rect(self.sprite_rect.topleft[0],self.sprite_rect.topleft[1],self.bounds[0],self.bounds[1])

    def move(self, displacement):
        self.sprite_rect = self.sprite_rect.move(displacement)