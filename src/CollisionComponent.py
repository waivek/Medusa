import pygame

#this class is for pixel-perfect collision, for rect-based collision use MovingComponent

def print_mask(mask):
    size = mask.get_size()
    for i in range(size[1]):
        for j in range(size[0]):
            print(mask.get_at((j, i)), end="")
        print("")

class CollisionComponent:
    #obj must have a .sprite member
    def __init__(self, obj, level):
        self.obj = obj
        self.sprite = obj.sprite
        self.level = level

    #returns a collider if it colliders, otherwise returns None
    def check_collisions(self):
        colliders = list(self.level.colliders)

        from src.Skeleton import Skeleton
        if isinstance(self.obj.owner, Skeleton):
            colliders.append(self.level.players[0])
            if self.obj.owner in colliders:
                colliders.remove(self.obj.owner)

        my_mask = self.sprite.get_mask()
        my_rect = self.sprite.sprite_rect()

        # mask = pygame.Mask((100,100))
        # mask.clear()
        #mask.draw(my_mask,(0,0))
        #my_mask = mask

        #print("my")
        #print_mask(my_mask)

        for coll in colliders:
            their_mask = coll.sprite.get_mask()
            #print("their")
            #print_mask(their_mask)
            #their_mask.fill()
            their_rect = coll.sprite.sprite_rect()
            offset = (their_rect.topleft[0]-my_rect.topleft[0], their_rect.topleft[1]-my_rect.topleft[1])
            overlap = my_mask.overlap(their_mask,offset)
            my_mask.draw(their_mask,offset)

            #print("mask:")
            #if my_mask.count()>0:
            #    print_mask(my_mask)
            #print(overlap)
            if overlap is not None:
                return coll

        return None