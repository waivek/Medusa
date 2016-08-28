import pygame
import json

#todo - generate attach.txt
#todo - fix hand not rotating with arm

def import_json(path):
    file = open(path,'r+')
    lines = file.readlines()
    s = ""
    for i in lines:
        s += i
    j = json.loads(s)

    return j

def rotate_surface_around_point(surface, point, angle):
    result = pygame.Surface((2 * point[0], 2 * point[1]), pygame.SRCALPHA)
    result.fill((0, 0, 0, 0))
    result.blit(surface, (point[0]-16, point[1]-16, point[0]+16, point[1]+16))
    result = pygame.transform.rotate(result, angle)
    #size = result.get_size()
    #result = result.subsurface()
    #self.sprite_rec = self.sprite.get_rect(center=self.sprite_rec.center)
    #self.bounds = (0, 0, self.sprite_rec[2], self.sprite_rec[3])

    #if self.is_flipped:
    #    self.is_flipped = False
    #    self.flip()

    return result


def create_animation(path, head,arm,hand,leg, attach):
    anim = import_json("../raw/creator/anim/"+path+".json")
    frames = len(anim)

    body2arm = list(attach["body2arm"])
    arm2body = list(attach["arm2body"])
    arm2hand = list(attach["arm2hand"])
    hand2arm = list(attach["hand2arm"])
    body2leg = list(attach["body2leg"])
    leg2body = list(attach["leg2body"])

    #left
    left = pygame.Surface((32*frames, 32), pygame.SRCALPHA)
    left.fill((0, 0, 0, 0))

    for i in range(frames):
        fid = "frame"+str(i)

        leftarm_rot = anim[fid]["leftarm rot"]
        rightarm_rot = anim[fid]["rightarm rot"]
        lefthand_rot = anim[fid]["lefthand rot"]
        righthand_rot = anim[fid]["righthand rot"]
        leftleg_rot = anim[fid]["leftleg rot"]
        rightleg_rot = anim[fid]["rightleg rot"]

        # right
        tmp = rotate_surface_around_point(hand, hand2arm, righthand_rot)
        size = tmp.get_size()
        left.blit(tmp,
                  (32 * i + body2arm[0] - arm2body[0] + arm2hand[0] - hand2arm[0],
                   body2arm[1] - arm2body[1] + arm2hand[1] - hand2arm[1], 32, 32),
                  (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))

        tmp = rotate_surface_around_point(arm, arm2body, rightarm_rot)
        size = tmp.get_size()
        left.blit(tmp,
                  (32 * i + body2arm[0] - arm2body[0], body2arm[1] - arm2body[1], 32, 32),
                  (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))

        tmp = rotate_surface_around_point(leg, leg2body, rightleg_rot)
        size = tmp.get_size()
        left.blit(tmp,
                  (32 * i + body2leg[0] - leg2body[0], body2leg[1] - leg2body[1], 32, 32),
                  (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))

        # body
        left.blit(head, (32*i, 0, 32, 32))

        # left
        tmp = rotate_surface_around_point(leg, leg2body, leftleg_rot)
        size = tmp.get_size()
        left.blit(tmp,
                  (32 * i + body2leg[0] - leg2body[0], body2leg[1] - leg2body[1], 32, 32),
                  (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))
        
        tmp = rotate_surface_around_point(arm, arm2body, leftarm_rot)
        size = tmp.get_size()
        left.blit(tmp,
                  (32 * i + body2arm[0] - arm2body[0], body2arm[1] - arm2body[1], 32, 32),
                  (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))

        tmp = rotate_surface_around_point(hand, hand2arm, lefthand_rot)
        size = tmp.get_size()
        left.blit(tmp,
                  (32 * i + body2arm[0] - arm2body[0] + arm2hand[0] - hand2arm[0],
                   body2arm[1] - arm2body[1] + arm2hand[1] - hand2arm[1], 32, 32),
                  (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))


    #right
    right = pygame.Surface((32 * frames, 32), pygame.SRCALPHA)
    right.fill((0, 0, 0, 0))

    body2arm[0] = 32-body2arm[0]
    arm2body[0] = 32-arm2body[0]
    arm2hand[0] = 32-arm2hand[0]
    hand2arm[0] = 32-hand2arm[0]
    body2leg[0] = 32-body2leg[0]
    leg2body[0] = 32-leg2body[0]

    head = pygame.transform.flip(head,True,False)
    arm = pygame.transform.flip(arm, True, False)
    hand = pygame.transform.flip(hand, True, False)
    leg = pygame.transform.flip(leg, True, False)

    for i in range(frames):
        fid = "frame"+str(i)

        leftarm_rot = 360-anim[fid]["leftarm rot"]
        rightarm_rot = 360-anim[fid]["rightarm rot"]
        lefthand_rot = 360-anim[fid]["lefthand rot"]
        righthand_rot = 360-anim[fid]["righthand rot"]
        leftleg_rot = 360-anim[fid]["leftleg rot"]
        rightleg_rot = 360-anim[fid]["rightleg rot"]

        # left
        tmp = rotate_surface_around_point(hand, hand2arm, lefthand_rot)
        size = tmp.get_size()
        right.blit(tmp,
                   (32 * i + body2arm[0] - arm2body[0] + arm2hand[0] - hand2arm[0],
                    body2arm[1] - arm2body[1] + arm2hand[1] - hand2arm[1], 32, 32),
                   (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))

        tmp = rotate_surface_around_point(arm, arm2body, leftarm_rot)
        size = tmp.get_size()
        right.blit(tmp,
                   (32 * i + body2arm[0] - arm2body[0], body2arm[1] - arm2body[1], 32, 32),
                   (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))

        tmp = rotate_surface_around_point(leg, leg2body, leftleg_rot)
        size = tmp.get_size()
        right.blit(tmp,
                   (32 * i + body2leg[0] - leg2body[0], body2leg[1] - leg2body[1], 32, 32),
                   (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))

        # body
        right.blit(head, (32*i, 0, 32, 32))

        # right
        tmp = rotate_surface_around_point(leg, leg2body, rightleg_rot)
        size = tmp.get_size()
        right.blit(tmp,
                   (32 * i + body2leg[0] - leg2body[0], body2leg[1] - leg2body[1], 32, 32),
                   (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))

        tmp = rotate_surface_around_point(arm, arm2body, rightarm_rot)
        size = tmp.get_size()
        right.blit(tmp,
                   (32 * i + body2arm[0] - arm2body[0], body2arm[1] - arm2body[1], 32, 32),
                   (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))

        tmp = rotate_surface_around_point(hand, hand2arm, righthand_rot)
        size = tmp.get_size()
        right.blit(tmp,
                   (32 * i + body2arm[0] - arm2body[0] + arm2hand[0] - hand2arm[0],
                    body2arm[1] - arm2body[1] + arm2hand[1] - hand2arm[1], 32, 32),
                   (size[0] / 2 - 16, size[1] / 2 - 16, 32, 32))


    pygame.image.save(left, "../raw/creator/"+path+"_left.png")
    pygame.image.save(right, "../raw/creator/" + path + "_right.png")

def create_sprites():
    data = pygame.image.load(r"..\raw\creator\data.png", 'r')

    head = data.subsurface((0,0,32,32))
    arm1 = data.subsurface((32, 0, 32, 32))
    arm2 = data.subsurface((64, 0, 32, 32))
    leg = data.subsurface((96, 0, 32, 32))

    attach = import_json(r"..\raw\creator\attach.json")

    create_animation("walk", head, arm1, arm2, leg, attach)
    create_animation("jump", head, arm1, arm2, leg, attach)
    create_animation("stab", head, arm1, arm2, leg, attach)
    #create_animation("stand", head, arm1, arm2, leg, attach)
