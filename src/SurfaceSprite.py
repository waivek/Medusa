from src.WorldConstants import *

class SurfaceSprite:
    def __init__(self, surface):
        self.sprite = surface
        self.sprite_rec = self.sprite.get_rect()
        self.bounds = (0,0,self.sprite_rec[2],self.sprite_rec[3])
        #self.rotation = 0
        #self.is_flipped = False

    def draw(self,screen,camera):
        screen_rect = pygame.Rect(camera[0], camera[1], CONST_SCREEN_WIDTH, CONST_SCREEN_HEIGHT)
        if screen_rect.colliderect(self.sprite_rec):
            screen.blit(self.sprite, pygame.Rect(self.sprite_rec[0] - camera[0], self.sprite_rec[1] - camera[1],
                                                 self.sprite_rec[2] - camera[0],
                                                 self.sprite_rec[3] - camera[1]), pygame.Rect(self.bounds))

    def move(self, displacement):
        self.sprite_rec = self.sprite_rec.move(displacement)

    def set_location(self,pos):
        self.sprite_rec.topleft = pos

    def full_sprite_rect(self):
        return self.sprite_rec

    def sprite_rect(self):
        return pygame.Rect(self.sprite_rec.topleft[0]+self.bounds[0],self.sprite_rec.topleft[1]+self.bounds[1],self.bounds[2],self.bounds[3])

    def get_center(self):
        return (self.sprite_rec.topleft[0] + self.bounds[0] + int(self.bounds[2] / 2),
                self.sprite_rec.topleft[1] + self.bounds[1] + int(self.bounds[3] / 2))