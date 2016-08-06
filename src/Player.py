from src.Sprite import Sprite
import pygame

from enum import Enum
class PlayerState(Enum):
    GROUND = 0
    JUMPING = 1

class Player():
    def __init__(self, path_to_sprite, default_speed):
        self.velocity = (0, 0)
        self.acceleration = (0,0)
        self.default_speed = default_speed
        self.sprite = Sprite(path_to_sprite=path_to_sprite)
        self.position = self.sprite.sprite_rect.topleft
        self.state = PlayerState.JUMPING
        # self.sprite = pygame.image.load(path_to_sprite)
        # self.sprite_rect = self.sprite.get_rect()

    def draw(self, screen):
        self.sprite.draw(screen)

    def update_position(self, displacement):
        # self.sprite_rect = self.sprite_rect.move(displacement)
        self.sprite.move(displacement)
        newX = self.position[0] + displacement[0]
        newY = self.position[1] + displacement[1]
        self.position = (newX, newY)

    def update_velocity(self, acceleration):

        newX = self.velocity[0] + acceleration[0]
        newY = self.velocity[1] + acceleration[1]
        self.velocity = (newX, newY)

    def getpos(self):
        return self.position


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.velocity = (-self.default_speed, self.velocity[1])
            if event.key == pygame.K_RIGHT:
                self.velocity = (self.default_speed, self.velocity[1])
            if event.key == pygame.K_SPACE and self.state==PlayerState.GROUND:
                self.velocity = (self.velocity[0],self.velocity[1]-300)
                self.state = PlayerState.JUMPING

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.velocity = (0, self.velocity[1])

    def set_acceleration(self,acc):
        self.acceleration=acc

    def update(self, deltaTime):



        a = self.sprite.sprite_rect.topleft
        b = self.position
        print("sprite_rect = %f %f" % (self.sprite.sprite_rect.topleft[0], self.sprite.sprite_rect.topleft[1]))
        print("position = %f %f" % (self.position[0], self.position[1]))
        # assert(abs(a[0] - b[0]) < 1)
        # assert(abs(a[1] - b[1]) < 1)
        dt = deltaTime / 1000
        self.update_velocity(((self.acceleration[0] * dt, self.acceleration[1] * dt)))
        self.update_position((self.velocity[0] * dt, self.velocity[1] * dt))

        if self.state == PlayerState.JUMPING:
            self.acceleration = (self.acceleration[0], 250)
        elif self.state == PlayerState.GROUND:
            self.velocity = (self.velocity[0], 0)
            self.acceleration = (self.acceleration[0], 0)



