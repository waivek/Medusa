import pygame

class Timer:
    def __init__(self):
        self.ticks = 0
        self.start_time = pygame.time.get_ticks()

    def get_time(self):
        tmp = pygame.time.get_ticks()
        self.ticks += tmp - self.start_time
        self.start_time = tmp
        return self.ticks

    def reset(self):
        self.ticks = 0
        self.start_time = pygame.time.get_ticks()

    def mod_time(self, frequency):
        self.ticks = self.ticks%frequency