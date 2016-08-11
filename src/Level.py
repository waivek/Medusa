from src.Sprite import *
from src.Player import *
from src.Monster import *
from src.Skeleton import *
from src.LoadResources import *
from src.HUD import *
import src.Util
import pygame

class Level:
    def __init__(self, row, col):
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
        #self.map[8][9] = True
        #self.map[9][9] = True
        #self.map[10][9] = True

        self.map[5][10] = True
        self.map[6][10] = True
        self.map[7][10] = True
        #self.map[8][10] = True
        #self.map[9][10] = True
        #self.map[10][10] = True

        self.map[10][12] = False
        self.map[11][12] = False
        self.map[12][12] = False
        self.map[10][13] = False
        self.map[11][13] = False
        self.map[12][13] = False
        self.map[10][14] = False

        self.sky_sprite = Sprite(ImageEnum.SKY)
        self.block_sprite = Sprite(ImageEnum.BLOCK)
        self.camera_pos = (32*10, 0)

        self.monsters = []
        self.players = []

        p = Player(self.map,self.col,self.row)
        m = Skeleton(self.map, self.col, self.row)
        self.add_player(p)
        self.add_monster(m)

        self.hud = HUD(self.players[0])

    def add_player(self, player):
        assert isinstance(player, Player)
        self.players.append(player)

    def add_monster(self, monster):
        #assert isinstance(monster, Monster)
        self.monsters.append(monster)

    def draw(self, screen):
        self.sky_sprite.draw(screen, (0,0))

        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] is True:
                    self.block_sprite.set_location((BLOCK_SIZE*j,BLOCK_SIZE*i))
                    self.block_sprite.draw(screen,self.camera_pos)

        for player in self.players:
            player.draw(screen,self.camera_pos)

        for monster in self.monsters:
            monster.draw(screen,self.camera_pos)

        self.hud.draw(screen)

    def handle_event(self, event):
        for player in self.players:
            player.handle_event(event)

    def point_in_wall(self, x, y):
        for i in range(self.col):
            for j in range(self.row):
                if self.map[j][i]:
                    tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
                    if src.Util.point_in_rect((x,y),tile_rect):
                        return True
        return False

    def update(self, deltatime):
        #update entities and detect collision
        for player in self.players:
            player.update(deltatime)

        for monster in self.monsters:
            monster.update(deltatime)

        #update camera
        self.camera_pos = (self.players[0].moving_component.position[0]-CONST_CAMERA_PLAYER_OFFSET, self.camera_pos[1])