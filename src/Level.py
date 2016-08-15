from src.Sprite import *
from src.Player import *
from src.Monster import *
from src.Powerup import *
from src.LoadResources import *
from src.HUD import *
from src.Powerups import *
import src.Util
import pygame

class Level:
    def __init__(self):
        self.row = 100
        self.col = 100
        self.map = \
            [
                [ y >= (10) for x in range(self.col)]
                for y in range(self.row)
            ]

        self.sky_sprite = Sprite(ImageEnum.SKY)
        self.sky_sprite.bounds = (0,0,2000,2000)

        self.block_sprite = Sprite(ImageEnum.BLOCK)
        self.camera_pos = (32*10, 0)

        self.monsters = []
        self.players = []
        self.entities = []

        for i in range(self.col):
            self.map[0][i] = True
            self.map[i][0] = True
            self.map[99][i] = True
            self.map[i][99] = True

        self.map[1][9] = True
        self.map[2][9] = True
        self.map[3][9] = True
        self.map[4][9] = True
        self.map[5][9] = True
        self.map[6][9] = True
        self.map[8][9] = True
        self.map[7][9] = True
        self.map[7][8] = True
        self.map[7][7] = True
        self.map[7][6] = True
        self.map[7][5] = True
        self.map[7][4] = True
        self.map[7][3] = True
        self.map[7][2] = True

        e = Player((32,32), self)
        e.moving_component.move((32,32))
        self.add_player(e)

        k = Key(KeyEnum.DARK, (32 * 6, 32 * 5))
        self.add_entity(k)

        k = Lock(KeyEnum.DARK, (32 * 9, 32 * 9))
        self.add_entity(k)

        self.hud = HUD(self.players[0])
        self.show_hud = True

    def destroy_entity(self, target):
        self.entities.remove(target)

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_player(self, player):
        assert isinstance(player, Player)
        self.players.append(player)
        self.entities.append(player)

    def add_monster(self, monster):
        #assert isinstance(monster, Monster)
        self.monsters.append(monster)
        self.entities.append(monster)

    def add_powerup(self, powerup):
        assert isinstance(powerup, Powerup)
        self.entities.append(powerup)

    def draw(self, screen):
        self.sky_sprite.draw(screen, (0,0))

        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] is True:
                    self.block_sprite.set_location((BLOCK_SIZE*j,BLOCK_SIZE*i))
                    self.block_sprite.draw(screen,self.camera_pos)


        #for monster in self.monsters:
        #    monster.draw(screen,self.camera_pos)

        for entity in self.entities:
            entity.draw(screen, self.camera_pos)

        if self.show_hud:
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
        for entity in self.entities:
            entity.update(deltatime)

        #update camera
        self.camera_pos = (self.players[0].moving_component.position[0] - CONST_CAMERA_PLAYER_OFFSET_X, 0)
        # self.camera_pos = (0, 0)
