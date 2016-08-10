from src.Sprite import Sprite
from src.Player import PlayerState
from src.Player import BLOCK_SIZE
from src.Player import CONST_CAMERA_PLAYER_OFFSET
from src.LoadResources import ImageEnum
from src.LoadResources import gImages
import src.Util
import pygame

class Level:
    def __init__(self, row, col):
        self.player1 = None
        self.player2 = None
        self.row = row
        self.col = col
        self.map = \
            [
                [ y >= (self.row / 2) for x in range(self.col)]
                for y in range(self.row)
            ]
        self.map[5][5] = False
        self.map[5][6] = False
        self.map[5][7] = True
        self.map[5][8] = True
        self.map[5][9] = True
        self.map[6][9] = True
        self.map[7][9] = True
        self.map[8][9] = True
        self.map[9][9] = True
        self.map[10][9] = True

        self.map[5][10] = True
        self.map[6][10] = True
        self.map[7][10] = True
        self.map[8][10] = True
        self.map[9][10] = True
        self.map[10][10] = True

        self.sky_sprite = Sprite(ImageEnum.SKY)
        self.block_sprite = Sprite(ImageEnum.BLOCK)
        self.camera_pos = (32*10, 0)

    def add_player(self, player):
        if self.player1 is None:
            self.player1 = player
        elif self.player2 is None:
            self.player2 = player
        else:
            raise Exception("Tried to add player>2")

    def draw(self, screen):
        self.sky_sprite.draw(screen, (0,0))

        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] is True:
                    self.block_sprite.set_location((BLOCK_SIZE*j,BLOCK_SIZE*i))
                    self.block_sprite.draw(screen,self.camera_pos)

        if self.player1 is not None:
            self.player1.draw(screen,self.camera_pos)
        if self.player2 is not None:
            self.player2.draw(screen,self.camera_pos)

    def handle_event(self, event):
        if self.player1 is not None:
            self.player1.handle_event(event)
        if self.player2 is not None:
            self.player2.handle_event(event)

    def point_in_wall(self, x, y):
        for i in range(self.col):
            for j in range(self.row):
                if self.map[j][i]:
                    tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
                    if src.Util.point_in_rect((x,y),tile_rect):
                        return True
        return False

    def get_pushout(self, position, rect):
        target = src.Util.push_out(position[0],position[1],rect)
        target = (target[0]-position[0],target[1]-position[1])
        return target

    def update(self, deltatime):
        #print(self.player1.velocity)
        #update player and detect collision
        if self.player1 is not None:
            # flag = 0
            # target = (self.player1.position[0] + self.player1.velocity[0], self.player1.position[1], self.player1.velocity[1])
            # while flag == 0:
            #     flag = 1
            #     for i in range(self.col):
            #         if flag == 0:
            #             break
            #         for j in range(self.row):
            #             if self.map[j][i]:
            #                 tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
            #                 if src.Util.rect_intersect(self.player1.getrekt(),tile_rect):
            #
            #                     print("pushing from %d %d" % (i, j))
            #
            #                     pushout = self.get_pushout(self.player1.sprite.sprite_rect().topleft, tile_rect)
            #                     target = (target[0] + pushout[0], target[1] + pushout[1])
            #                     displacement = (target[0] - self.player1.position[0], target[1] - self.player1.position[1])
            #                     self.player1.update_position(displacement,self.map,self.col,self.row)
            #                     print(displacement)
            #
            #                     pushout = self.get_pushout(self.player1.sprite.sprite_rect().topright, tile_rect)
            #                     target = (target[0] + pushout[0], target[1] + pushout[1])
            #                     displacement = (target[0] - self.player1.position[0], target[1] - self.player1.position[1])
            #                     self.player1.update_position(displacement,self.map,self.col,self.row)
            #                     print(displacement)
            #
            #                     pushout = self.get_pushout(self.player1.sprite.sprite_rect().bottomleft, tile_rect)
            #                     target = (target[0] + pushout[0], target[1] + pushout[1])
            #                     displacement = (target[0] - self.player1.position[0], target[1] - self.player1.position[1])
            #                     self.player1.update_position(displacement,self.map,self.col,self.row)
            #                     print(displacement)
            #
            #                     pushout = self.get_pushout(self.player1.sprite.sprite_rect().bottomright, tile_rect)
            #                     target = (target[0] + pushout[0], target[1] + pushout[1])
            #                     displacement = (target[0] - self.player1.position[0], target[1] - self.player1.position[1])
            #                     self.player1.update_position(displacement,self.map,self.col,self.row)
            #
            #                     print(displacement)
                                #self.player1.velocity = (self.player1.velocity[0],0)
                                #self.player1.velocity = (0, self.player1.velocity[1])

                            #flag = 0
                            #break


            # flag = 0
            # flag2 = 0
            #
            # while flag==0:
            #     flag = 1
            #     for i in range(self.col):
            #         if(flag==0):
            #             break
            #         for j in range(self.row):
            #             if self.map[j][i]:
            #                 tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
            #                 player_rect = self.player1.getrekt()
            #                 player_rect = pygame.Rect(player_rect.topleft[0]+self.player1.velocity[0],player_rect.topleft[1]+self.player1.velocity[1],
            #                                         player_rect.bottomright[0] + self.player1.velocity[0],
            #                                         player_rect.bottomright[1] + self.player1.velocity[1])
            #
            #                 #player_rect.bottomright = (player_rect.bottomright[0] + self.player1.velocity[0],
            #                 #                       player_rect.bottomright[1] + self.player1.velocity[1])
            #                 if src.Util.rect_intersect(player_rect, tile_rect):
            #                     (vertical_x, horizontal_y) = src.Util.get_intersecting_lines(player_rect,
            #                                                                         tile_rect)
            #
            #                     (p_x, p_y) = src.Util.get_inner_point(player_rect, tile_rect)
            #
            #                     v_x = -self.player1.velocity[0]
            #                     v_y = -self.player1.velocity[1]
            #                     #v_x = -self.player1.velocity[0]
            #                     #v_y = -self.player1.velocity[1]
            #                     if self.point_in_wall( self.player1.position[0], self.player1.oldposition[1] ):
            #                         v_x = 0
            #                     if self.point_in_wall( self.player1.oldposition[0], self.player1.position[1] ):
            #                         v_y = 0
            #                     if(v_x == 0 and v_y == 0):
            #                         v_x = -self.player1.position[0] - self.player1.oldposition[0]
            #                         v_y = -self.player1.position[1] - self.player1.oldposition[1]
            #                     #else:
            #                     #    print("collision ERROR: both points outside wall")
            #
            #                     (target_x, target_y) = src.Util.get_target_point(
            #                         vertical_x, horizontal_y,
            #                         v_x, v_y,
            #                         p_x, p_y
            #                     )
            #                     print("tx, ty:")
            #                     print((target_x,target_y))
            #                     print("p1 pos : %d %d" % (self.player1.position[0],self.player1.position[1]))
            #                     self.player1.update_position((target_x - p_x, target_y - p_y))
            #                     print("p2 pos : %d %d" % (self.player1.position[0], self.player1.position[1]))
            #
            #                     if abs(target_y - horizontal_y) <= 1 and self.player1.velocity[1] > 64:
            #                         self.player1.state = PlayerState.GROUND
            #                         self.player1.update_sprite()
            #
            #                     if (abs(self.player1.velocity[1]) > 64):
            #                         self.player1.velocity = (self.player1.velocity[0], 0)
            #
            #                     if abs(target_y - horizontal_y) <= 1:
            #                         self.player1.velocity = (self.player1.velocity[0],0)
            #                     if abs(target_x - vertical_x) <= 1:
            #                         self.player1.velocity = (0,self.player1.velocity[1])
            #
            #                     #else:
            #                     #    self.player1.state = PlayerState.JUMPING
            #                     flag = 0
            #                     flag2 = 1
            #                     print("inside rect: %d %d" % (i,j))
            #                     #print("-vel: %d %d" % (v_x,v_y))
            #                     break
            #
            #                     #continue
            #if flag2==0:
            self.player1.update(deltatime, self.map, self.col, self.row)

        if self.player2 is not None:
            self.player2.update(deltatime)

        #update camera
        self.camera_pos = (self.player1.position[0]-CONST_CAMERA_PLAYER_OFFSET, self.camera_pos[1])