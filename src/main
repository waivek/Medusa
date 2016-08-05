import sys
import pygame
from src.Player import Player

def main():
    pygame.init()

    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    black = 0, 0, 0
    p1 = Player(path_to_sprite="..\\raw\\sprite.jpg", default_speed=100)
    print(p1.__class__)
    time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            p1.handleEvent(event)
        screen.fill(black)
        deltaTime = pygame.time.get_ticks() - time
        while deltaTime < 16:
            deltaTime = pygame.time.get_ticks() - time
        time = pygame.time.get_ticks()
        p1.Update(deltaTime)
        p1.draw(screen)
        pygame.display.flip()

main()
