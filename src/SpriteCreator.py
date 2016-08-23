import pygame

def create_sprites():
    data = pygame.image.load(r"..\raw\creator\data.png", )

    head = data.subsurface((0,0,32,32))
    arm1 = data.subsurface((32, 0, 32, 32))
    arm2 = data.subsurface((64, 0, 32, 32))
    leg = data.subsurface((96, 0, 32, 32))

    result = pygame.Surface((32,32), pygame.SRCALPHA)
    result.fill((0,0,0,0))

    result.blit(arm1, (-5,-5,32,32))
    result.blit(arm2, (2, -1, 32, 32))
    result.blit(leg, (3, 5, 32, 32))

    result.blit(head,(0,0,32,32))

    result.blit(arm1, (-5, -5, 32, 32))
    result.blit(arm2, (2, -1, 32, 32))
    result.blit(leg, (3, 5, 32, 32))

    pygame.image.save(result,r"..\raw\creator\result.png")