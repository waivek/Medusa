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
    p1 = Player(path_to_sprite="..\\raw\\player1.png", default_speed=100)
    level.add_player(p1)
    time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            # p1.handleEvent(event)
            level.handle_event(event)
        screen.fill(black)
        deltaTime = pygame.time.get_ticks() - time
        while deltaTime < 16:
            deltaTime = pygame.time.get_ticks() - time
        print(deltaTime)
        time = pygame.time.get_ticks()
        # p1.Update(deltaTime)
        # p1.draw(screen)
        level.update(deltaTime)
        level.draw(screen)
        pygame.display.flip()

main()
