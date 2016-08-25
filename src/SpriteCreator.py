import pygame
import json

def import_animation(path):
    file = open(path,'r+')
    lines = file.readlines()
    s = ""
    for i in lines:
        s += i
    j = json.loads(s)

    return j

def create_animation(path, head,arm1,arm2,leg):
    j = import_animation(path)
    frames = len(j)

    result = pygame.Surface((32*frames, 32), pygame.SRCALPHA)
    result.fill((0, 0, 0, 0))

    for i in range(frames):
        fid = "frame"+str(i)
        body2arm = j[fid]["body2arm"]
        arm2body = j[fid]["arm2body"]
        arm2hand = j[fid]["arm2hand"]
        hand2arm = j[fid]["hand2arm"]
        body2leg = j[fid]["body2leg"]
        leg2body = j[fid]["leg2body"]

        # left
        result.blit(arm1, (32*i + body2arm[0]-arm2body[0], body2arm[1]-arm2body[0], 32, 32))
        result.blit(arm2, (32*i + body2arm[0]-arm2body[0] + arm2hand[0]-hand2arm[0],
                           body2arm[1]-arm2body[0] + arm2hand[1]-hand2arm[0], 32, 32))
        result.blit(leg, (32*i + body2leg[0]-leg2body[0], body2leg[1]-leg2body[0], 32, 32))

        # body
        result.blit(head, (32*i, 0, 32, 32))

        # right
        result.blit(arm1, (32*i + body2arm[0] - arm2body[0], body2arm[1] - arm2body[0], 32, 32))
        result.blit(arm2, (32*i + body2arm[0] - arm2body[0] + arm2hand[0] - hand2arm[0],
                           body2arm[1] - arm2body[0] + arm2hand[1] - hand2arm[0], 32, 32))
        result.blit(leg, (32*i + body2leg[0] - leg2body[0], body2leg[1] - leg2body[0], 32, 32))

    return result

def create_sprites():
    data = pygame.image.load(r"..\raw\creator\data.png", )

    head = data.subsurface((0,0,32,32))
    arm1 = data.subsurface((32, 0, 32, 32))
    arm2 = data.subsurface((64, 0, 32, 32))
    leg = data.subsurface((96, 0, 32, 32))

    result = create_animation(r"../raw/creator/anim/walk_left.json",head,arm1,arm2,leg)

    pygame.image.save(result,r"..\raw\creator\result.png")