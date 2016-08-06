import sys
import pygame
from src.Level import Level
from src.Player import Player
from src.LoadResources import load_resources

def init():
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    if not load_resources():
        print("ERROR: unable to load resources")

def main():
    init()

    size = 800, 400
    screen = pygame.display.set_mode(size)
    black = 0, 0, 0
    level = Level(20, 100)
    p1 = Player()
    level.add_player(p1)
    time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                sys.exit()
            if event == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            level.handle_event(event)
        screen.fill(black)
        deltatime = pygame.time.get_ticks() - time
        while deltatime < 16:
            deltatime = pygame.time.get_ticks() - time

        time = pygame.time.get_ticks()

        level.update(deltatime)
        level.draw(screen)
        pygame.display.flip()

main()
