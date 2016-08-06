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
        print("next frame: %d %d" % (self.current_frame,self.max_frames))

    def reset(self):
        self.current_frame = 0
        self.timer.reset()

    def update(self, deltatime):
        time = self.timer.get_time()
        print("abcd %d" % time)
        if time >= self.frequency:
            self.timer.mod_time(self.frequency)
            self.next_frame()

    def draw(self, screen):
        print("curr frame: %d" % self.current_frame)
        rect = pygame.Rect((self.current_frame*self.bounds[0],0),self.bounds)
        screen.blit(gImages[self.image_id.value], self.sprite_rect, rect)
        print(self.sprite_rect)

    def move(self, displacement):
        self.sprite_rect = self.sprite_rect.move(displacement)