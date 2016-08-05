import pygame

class Sprite():
    def __init__(self, path_to_sprite):
        self.sprite = pygame.image.load(path_to_sprite)
        self.sprite_rect = self.sprite.get_rect()

    def move(self, displacement):
        self.sprite_rect = self.sprite_rect.move(displacement)

    def draw(self, screen):
        screen.blit(self.sprite, self.sprite_rect)


