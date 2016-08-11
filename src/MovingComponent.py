from src.WorldConstants import *
import pygame

class MovingComponent:
    def __init__(self, sprite, tiles, col, row):
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0,0)
        self.sprite = sprite
        self.size = (BLOCK_SIZE, BLOCK_SIZE)

        self.tiles = tiles
        self.tiles_col = col
        self.tiles_row = row

        self.in_air = False
        self.gravity = CONST_GRAVITY

    def point_in_wall(self, x, y):
        cx = int(x/32)
        cy = int(y/32)
        if self.tiles[cy][cx]:
            return True
        return False

    def snap_out(self):
        m = 0
        flag = 0
        factor = 1
        while flag==0:
            for i in range(2*m+1):
                if flag==1:
                    break
                for j in range(2*m+1):
                    d = (factor*(int(i/2)*((-1)**(i%2))),factor*(int(j/2)*((-1)**(j%2))))
                    b = False
                    b = b or self.point_in_wall(self.sprite.sprite_rect().topleft[0] + d[0],self.sprite.sprite_rect().topleft[1] + d[1])
                    b = b or self.point_in_wall(self.sprite.sprite_rect().topright[0] + d[0],self.sprite.sprite_rect().topright[1] + d[1])
                    b = b or self.point_in_wall(self.sprite.sprite_rect().bottomleft[0] + d[0],self.sprite.sprite_rect().bottomleft[1] + d[1])
                    b = b or self.point_in_wall(self.sprite.sprite_rect().bottomright[0] + d[0],self.sprite.sprite_rect().bottomright[1] + d[1])

                    if b is False:
                        self.move(d)
                        if (d[0] is not 0):
                            self.velocity = (0, self.velocity[1])
                        if (d[1] is not 0):
                            self.velocity = (self.velocity[0], 0)
                        print(m)
                        flag=1
                        break
            m += 1

    def move(self, displacement):
        self.sprite.move(displacement)
        newx = self.position[0] + int(displacement[0])
        newy = self.position[1] + int(displacement[1])
        self.position = (newx, newy)

    def update_position(self, displacement):
        old_pos = self.position

        #update position
        self.move(displacement)

        #check for collisions
        self.snap_out()

        #check if falling
        if old_pos[1]==self.position[1]:
            self.in_air = False
        else:
            self.in_air = True

    def update_velocity(self, acceleration):
        newx = self.velocity[0] + acceleration[0]
        newy = self.velocity[1] + acceleration[1]

        #cap the velocity
        if(newx>CONST_MAX_VELOCITY):
            newx = CONST_MAX_VELOCITY
        if(newy>CONST_MAX_VELOCITY):
            newy=CONST_MAX_VELOCITY

        self.velocity = (newx, newy)

    def update(self, deltatime):
        dt = deltatime / 1000

        # update parameters
        self.update_position((self.velocity[0] * dt, self.velocity[1] * dt))
        self.update_velocity(((self.acceleration[0] * dt, self.acceleration[1] * dt)))

        self.acceleration = (self.acceleration[0], self.gravity)
