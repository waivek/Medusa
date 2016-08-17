import pygame

#this class is for pixel-perfect collision, for rect-based collision use MovingComponent

class CollisionComponent:
    #obj must have a .sprite member
    def __init__(self, obj, level):
        self.obj = obj
        self.sprite = obj.sprite
        self.level = level

    #returns a collider if it colliders, otherwise returns None
    def check_collisions(self):
        colliders = self.level.colliders
        my_mask = self.sprite.get_mask()
        my_rect = self.sprite.sprite_rect()
        for i in colliders:
            their_mask = i.sprite.get_mask()
            their_rect = i.sprite.sprite_rect()

            offset = (their_rect.topleft[0]-my_rect.topleft[0], their_rect.topleft[1]-my_rect.topleft[1])

            if my_mask.overlap(their_mask,offset) is not None:
                return i

        return None