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
        # self.map[5][5] = True
        # self.map[5][6] = True
        # self.map[5][7] = True
        # self.map[5][8] = True
        # self.map[5][9] = True

        # self.map[6][5] = True
        # self.map[7][5] = True
        # self.map[8][5] = True
        # self.map[9][5] = True

        self.sky_sprite = Sprite(ImageEnum.SKY)
        self.block_sprite = Sprite(ImageEnum.BLOCK)
        self.camera_pos = (32*10, 0)
        self.monsters = []

    def add_monster(self, monster):
        self.monsters.append(monster)


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

        for monster in self.monsters:
            monster.draw(screen, self.camera_pos)


    def handle_event(self, event):
        if self.player1 is not None:
            self.player1.handle_event(event)
        if self.player2 is not None:
            self.player2.handle_event(event)

    def update(self, deltatime):
        #update player and detect collision
        if self.player1 is not None:
            self.player1.update(deltatime)

            for i in range(self.col):
                for j in range(self.row):
                    if self.map[j][i]:
                        tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
                        player_rect = self.player1.getrekt()

                        if src.Util.rect_intersect(player_rect, tile_rect):
                            (vertical_x, horizontal_y) = src.Util.get_intersecting_lines(player_rect,
                                                                                tile_rect)

                            (p_x, p_y) = src.Util.get_inner_point(player_rect, tile_rect)

                            (target_x, target_y) = src.Util.get_target_point(
                                vertical_x = vertical_x, horizontal_y = horizontal_y,
                                v_x= -self.player1.moving_component.velocity[0], v_y= -self.player1.moving_component.velocity[1],
                                p_x = p_x, p_y = p_y
                            )

                            self.player1.moving_component.update_position((target_x - p_x, target_y - p_y))

                            if abs(target_y - horizontal_y) <= 1 and self.player1.moving_component.velocity[1] > 64:
                                self.player1.state = PlayerState.GROUND
                                self.player1.update_sprite()

                            if (abs(self.player1.moving_component.velocity[1]) > 64):
                                self.player1.moving_component.velocity = (self.player1.moving_component.velocity[0], 0)
                            #else:
                            #    self.player1.state = PlayerState.JUMPING

        if self.player2 is not None:
            self.player2.update(deltatime)

        for monster in self.monsters:
            monster.update(deltatime)
            for i in range(self.col):
                for j in range(self.row):
                    if self.map[j][i]:
                        tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
                        player_rect = monster.getrekt()

                        if src.Util.rect_intersect(player_rect, tile_rect):
                            (vertical_x, horizontal_y) = src.Util.get_intersecting_lines(player_rect,
                                                                                         tile_rect)

                            (p_x, p_y) = src.Util.get_inner_point(player_rect, tile_rect)

                            (target_x, target_y) = src.Util.get_target_point(
                                vertical_x = vertical_x, horizontal_y = horizontal_y,
                                v_x= -monster.moving_component.velocity[0], v_y= -monster.moving_component.velocity[1],
                                p_x = p_x, p_y = p_y
                            )

                            monster.moving_component.update_position((target_x - p_x, target_y - p_y))

                            if abs(target_y - horizontal_y) <= 1 and monster.moving_component.velocity[1] > 64:
                                monster.set_to_ground()
                                monster.update_sprite()

                            if (abs(monster.moving_component.velocity[1]) > 64):
                                monster.moving_component.velocity = (monster.moving_component.velocity[0], 0)
                                #else:
                                #    monster.state = PlayerState.JUMPING


        #update camera
        self.camera_pos = (self.player1.moving_component.position[0]-CONST_CAMERA_PLAYER_OFFSET, self.camera_pos[1])
