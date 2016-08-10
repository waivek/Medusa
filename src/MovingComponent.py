from src.WorldConstants import *
import pygame

CONST_MAX_VELOCITY = 500

class MovingComponent:
    def __init__(self, sprite):
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0,0)
        self.sprite = sprite
        self.size = (BLOCK_SIZE, BLOCK_SIZE)

    def point_in_wall(self, x, y, tiles, col, row):
        #print("%d %d" % (x, y))
        cx = int(x/32)
        cy = int(y/32)
        if tiles[cy][cx]:
            return True
        return False
        # for i in range(col):
        #     for j in range(row):
        #         if tiles[j][i]:
        #             tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
        #             if src.Util.point_in_rect((x,y),tile_rect):
        #                 return True
        #             #else:
        #                 #print("false: %d %d %d %d" % (x,y,BLOCK_SIZE*i,BLOCK_SIZE*j))
        # return False

    def snap_out(self,tiles,col,row):
        m = 0
        flag = 0
        factor = 1
        while flag==0:
            print(m)
            for i in range(2*m+1):
                if flag==1:
                    break
                for j in range(2*m+1):
                    d = (factor*(int(i/2)*((-1)**(i%2))),factor*(int(j/2)*((-1)**(j%2))))
                    b = False
                    b = b or self.point_in_wall(self.sprite.sprite_rect().topleft[0] + d[0],self.sprite.sprite_rect().topleft[1] + d[1],tiles,col,row)
                    b = b or self.point_in_wall(self.sprite.sprite_rect().topright[0] + d[0],self.sprite.sprite_rect().topright[1] + d[1],tiles,col,row)
                    b = b or self.point_in_wall(self.sprite.sprite_rect().bottomleft[0] + d[0],self.sprite.sprite_rect().bottomleft[1] + d[1],tiles,col,row)
                    b = b or self.point_in_wall(self.sprite.sprite_rect().bottomright[0] + d[0],self.sprite.sprite_rect().bottomright[1] + d[1],tiles,col,row)

                    if b==False:
                        self.move(d)
                        #print("out")
                        #print(d)
                        if(d[0] != 0):
                            self.velocity = (0,self.velocity[1])
                        if (d[1] != 0):
                            self.velocity = (self.velocity[0], 1)
                        flag=1
                        break
            m = m + 1

    def move(self, displacement):
        self.sprite.move(displacement)
        #print("displ")
        #print(displacement)
        #print(self.position)
        newx = self.position[0] + int(displacement[0])
        newy = self.position[1] + int(displacement[1])
        self.position = (newx, newy)
        #print(self.position)

    def update_position(self, displacement, tiles, col, row):
        displacement = (int(displacement[0]),int(displacement[1]))

        #check for collisions
        # d1 = self.get_displacement(self.sprite.sprite_rect().topleft, displacement, tiles, row, col)
        # d2 = self.get_displacement(self.sprite.sprite_rect().topright, displacement, tiles, row, col)
        # d3 = self.get_displacement(self.sprite.sprite_rect().bottomleft, displacement, tiles, row, col)
        # d4 = self.get_displacement(self.sprite.sprite_rect().bottomright, displacement, tiles, row, col)
        #
        # print("d1")
        # print(self.sprite.sprite_rect().topleft)
        # print("d2")
        # print(self.sprite.sprite_rect().topright)
        # print("d3")
        # print(self.sprite.sprite_rect().bottomleft)
        # print("d4")
        # print(self.sprite.sprite_rect().bottomright)
        # dx = min([d1[0],d2[0],d3[0],d4[0]])
        # dy = min([d1[1],d2[1],d3[1],d4[1]])
        #
        #
        # dis_old = displacement
        #
        # displacement = (dx,dy)
        # #print("displacement")
        # #print(displacement)
        #
        # if(dis_old[0]!=displacement[0]):
        #     self.velocity = (0, self.velocity[1])
        #     print("player rect")
        #     print(self.sprite.sprite_rect())
        #
        # if(dis_old[1]!=displacement[1]):
        #     self.velocity = (self.velocity[0], 1)
        #     print("player rect")
        #     print(self.sprite.sprite_rect())
        #update position
        self.sprite.move(displacement)
        newx = self.position[0] + int(displacement[0])
        newy = self.position[1] + int(displacement[1])
        self.position = (newx, newy)

        self.snap_out(tiles,col,row)

    def update_velocity(self, acceleration):
        newx = self.velocity[0] + acceleration[0]
        newy = self.velocity[1] + acceleration[1]

        #cap the velocity
        if(newx>CONST_MAX_VELOCITY):
            newx = CONST_MAX_VELOCITY
        if(newy>CONST_MAX_VELOCITY):
            newy=CONST_MAX_VELOCITY

        self.velocity = (newx, newy)

    def update(self, deltatime, tiles, col, row):

        dt = deltatime / 1000
        print(self.position)

        # update parameters
        self.update_position((self.velocity[0] * dt, self.velocity[1] * dt), tiles, col, row)
        self.update_velocity(((self.acceleration[0] * dt, self.acceleration[1] * dt)))

        self.acceleration = (self.acceleration[0], CONST_GRAVITY)
