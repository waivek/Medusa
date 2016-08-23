import sys
from src.MapEditor import *
import src.SpriteCreator

CONST_MAX_FPS = 60
CONST_DELTATIME_MAX = 50

#todo - pixel perfect collision for arrow against wall
#todo - sound and particle effects for combat
#todo - fix double jump bug
#done - fix skeleton collision vs. lock
#done - unable attack from right side bug
#todo - remove hat from jumping animation
#todo - make collider masks pixel perfect
#done - fix weapon swapping bug
#done - fix weapon attach points not working properly
#todo - fix ammo system

def init():
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

    if not load_resources():
        print("ERROR: unable to load resources")

    init_weapons()

def main():
    src.SpriteCreator.create_sprites()

    init()

    size = CONST_SCREEN_WIDTH, CONST_SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    black = 0, 0, 0
    level = Level.load(r"..\level.txt")
    #level = MapEditor()
    #p1 = Player(level.map,level.col,level.row, level)
    #level.add_player(p1)
    #level.add_monster(Skeleton(level.map,level.col,level.row))
    time = pygame.time.get_ticks()

    lastsecond = time
    frames = 0

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
        while deltatime < 1000/CONST_MAX_FPS:
            deltatime = pygame.time.get_ticks() - time

        time = pygame.time.get_ticks()

        if deltatime > CONST_DELTATIME_MAX:
            deltatime = CONST_DELTATIME_MAX

        level.update(deltatime)
        level.draw(screen)
        pygame.display.flip()

        frames += 1
        if time - lastsecond > 1000:
            lastsecond = time
            print("FPS: %d" % frames)
            frames = 0

main()
