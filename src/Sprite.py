import pygame
from src.LoadResources import ImageEnum

class Sprite:
    def __init__(self, path_to_sprite):
        self.sprite = pygame.image.load(path_to_sprite)
        self.sprite_rect = self.sprite.get_rect()

    def move(self, displacement):
        self.sprite_rect = self.sprite_rect.move(displacement)

    def set_location(self,pos):
        self.sprite_rect.topleft = pos

    def draw(self, screen):
        screen.blit(self.sprite, self.sprite_rect)

def rect_intersect(rect1, rect2):
    flag = 0
    if rect1.topleft[0] >= rect2.topleft[0] \
            and rect1.topleft[0] <= rect2.bottomright[0]:
        flag = 1
    if rect1.bottomright[0] >= rect2.topleft[0] \
            and rect1.bottomright[0] <= rect2.bottomright[0]:
        flag = 1
    if flag == 1:
        if rect1.topleft[1] >= rect2.topleft[1] \
                and rect1.topleft[1] <= rect2.bottomright[1]:
            return True
        if rect1.bottomright[1] >= rect2.topleft[1] \
                and rect1.bottomright[1] <= rect2.bottomright[1]:
            return True
    return False

