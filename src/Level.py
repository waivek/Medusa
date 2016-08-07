from src.Sprite import Sprite
from src.Player import PlayerState
from src.Player import BLOCK_SIZE
from src.LoadResources import ImageEnum
from src.LoadResources import gImages
import src.Util
import pygame

class Level:
    def __init__(self, row, col):
        self.monsters = []

        self.player1 = None
        self.player2 = None
        self.row = row
        self.col = col
        self.map = \
            [
                [ y >= (self.row / 2) for x in range(self.col)]
                for y in range(self.row)
            ]

        self.sky_sprite = Sprite(ImageEnum.SKY)
        self.block_sprite = Sprite(ImageEnum.BLOCK)

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
        self.sky_sprite.draw(screen)

        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] is True:
                    self.block_sprite.set_location((BLOCK_SIZE*j,BLOCK_SIZE*i))
                    self.block_sprite.draw(screen)

        if self.player1 is not None:
            self.player1.draw(screen)
        if self.player2 is not None:
            self.player2.draw(screen)

        for monster in self.monsters:
            monster.draw(screen)


    def handle_event(self, event):
        if self.player1 is not None:
            self.player1.handle_event(event)
        if self.player2 is not None:
            self.player2.handle_event(event)

    def handle_collisions(self, entity, tile_rect):
        player_rect = entity.getrekt()

        if src.Util.rect_intersect(player_rect, tile_rect):
            (vertical_x, horizontal_y) = src.Util.get_intersecting_lines(player_rect,
                                                                         tile_rect)

            (p_x, p_y) = src.Util.get_inner_point(player_rect, tile_rect)

            (target_x, target_y) = src.Util.get_target_point(
                vertical_x=vertical_x, horizontal_y=horizontal_y,
                v_x= -entity.velocity[0], v_y= -entity.velocity[1],
                p_x=p_x, p_y=p_y
            )

            entity.update_position((target_x - p_x, target_y - p_y))

            if(entity.velocity[1] > 0):
                entity.velocity = (entity.velocity[0],0)
            #if target_y == horizontal_y:

            entity.set_to_ground()
            # entity.state = PlayerState.GROUND
            #elif target_x == vertical_x:
            #    entity.state = PlayerState.JUMPING


    def update(self, deltatime):
        if self.player1 is not None:
            self.player1.update(deltatime)

        if self.player2 is not None:
            self.player2.update(deltatime)

        for monster in self.monsters:
            monster.update(deltatime)

        for i in range(self.col):
            for j in range(self.row):
                if self.map[j][i]:
                    tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
                    self.handle_collisions(self.player1, tile_rect)
                    for monster in self.monsters:
                        self.handle_collisions(monster, tile_rect)

