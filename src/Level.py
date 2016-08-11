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
        self.map[8][9] = True
        #self.map[9][9] = True
        #self.map[10][9] = True

        self.map[5][10] = True
        self.map[6][10] = True
        self.map[7][10] = True
        self.map[8][10] = True
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
        self.sky_sprite.bounds = (0,0,2000,2000)

        self.block_sprite = Sprite(ImageEnum.BLOCK)
        self.camera_pos = (32*10, 0)

        self.monsters = []
        self.players = []
        self.entities = []

        p = Player(self.map,self.col,self.row, self)
        m = Skeleton(self.map, self.col, self.row)
        self.add_player(p)
        self.add_monster(m)

        p = StaminaPowerup((32*9,32*9))
        self.add_powerup(p)

        p = GravityPowerup((15 * 22, 32 * 9))
        self.add_powerup(p)

        p = RegenPowerup((32 * 22, 32 * 9))
        self.add_powerup(p)

        p = SpringPowerup((32 * 19, 32 * 9))
        self.add_powerup(p)

        p = HastePowerup((32 * 2, 32 * 9))
        self.add_powerup(p)

        k = Key(KeyEnum.SILVER, (32* 5, 32*9))
        self.add_entity(k)

        k = Key(KeyEnum.DARK, (32 * 7, 32 * 9))
        self.add_entity(k)

        k = Lock(KeyEnum.SILVER, (32 * 10, 32 * 9))
        self.add_entity(k)

        self.hud = HUD(self.players[0])

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

        #for player in self.players:
        #    player.draw(screen,self.camera_pos)

        #for monster in self.monsters:
        #    monster.draw(screen,self.camera_pos)

        for entity in self.entities:
            entity.draw(screen, self.camera_pos)

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
        self.camera_pos = (self.players[0].moving_component.position[0]-CONST_CAMERA_PLAYER_OFFSET, self.camera_pos[1])