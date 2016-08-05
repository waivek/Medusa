import pygame

class Player():
    def __init__(self, path_to_sprite, default_speed):
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0,0)
        self.default_speed = default_speed
        self.sprite = pygame.image.load(path_to_sprite)
        self.sprite_rect = self.sprite.get_rect()

    def draw(self, screen):
        screen.blit(self.sprite, self.sprite_rect)

    def move(self, displacement):
        self.sprite_rect = self.sprite_rect.move(displacement)
        newX = self.position[0] + displacement[0]
        newY = self.position[1] + displacement[1]
        self.position = (newX, newY)

    def inertia(self, position):

        newX = self.velocity[0] + position[0]
        newY = self.velocity[1] + position[1]
        self.velocity = (newX, newY)


    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.velocity = (-self.default_speed, self.velocity[1])
            if event.key == pygame.K_RIGHT:
                self.velocity = (self.default_speed, self.velocity[1])
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.velocity = (0, self.velocity[1])

    def Update(self, deltaTime):
        dt = deltaTime / 1000
        self.inertia(((self.acceleration[0] * dt, self.acceleration[1] * dt)
        self.move((self.velocity[0] * dt, self.velocity[1] * dt))



