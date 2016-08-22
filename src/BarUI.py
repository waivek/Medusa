import pygame

class BarUI:
    def __init__(self, pos, color, height, scale):
        self.pos = pos
        self.color = color
        self.height = height
        self.scale = scale
        self.value = 0

    def draw(self, screen, camera):
        rect = pygame.Rect(self.pos[0]-camera[0],self.pos[1]-camera[1],int(self.value*self.scale),self.height)
        pygame.draw.rect(screen,self.color,rect)

    def update(self, value):
        self.value = value