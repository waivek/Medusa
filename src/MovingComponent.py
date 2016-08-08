from src.WorldConstants import *
import pygame

class MovingComponent:
    def __init__(self, sprite):
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0,0)
        self.sprite = sprite
        self.size = (BLOCK_SIZE, BLOCK_SIZE)

    def update_position(self, displacement):
        self.sprite.move(displacement)
        newx = self.position[0] + int(displacement[0])
        newy = self.position[1] + int(displacement[1])
        self.position = (newx, newy)


    def update_velocity(self, acceleration):
        newx = self.velocity[0] + acceleration[0]
        newy = self.velocity[1] + acceleration[1]
        self.velocity = (newx, newy)

    def update(self, deltaTime):
        dt = deltaTime / 1000
        self.update_position((self.velocity[0] * dt, self.velocity[1] * dt))
        self.update_velocity(((self.acceleration[0] * dt, self.acceleration[1] * dt)))
