from src.Sprite import *
from src.Player import *
from src.Monster import *
from src.Powerup import *
from src.LoadResources import *
from src.HUD import *
from src.Powerups import *
import src.Util
import pygame

class EntityEnum(Enum):
    PLAYER = 0
    SKELETON = 1
    REGEN_POWERUP = 2
    HASTE_POWERUP = 3
    STAMINA_POWERUP = 4
    GRAVITY_POWERUP = 5
    BOUNCE_POWERUP = 6
    KEY = 7
    LOCK = 8

EntityClasses = [Player,Skeleton,RegenPowerup,HastePowerup,StaminaPowerup,GravityPowerup,BouncePowerup,Key,Lock]

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

        self.hud = None
        self.show_hud = True

    def save_data(self, path):
        print("saving")
        file = open(path, 'r+')
        for i in range(self.col):
            for j in range(self.row):
                if self.map[j][i]:
                    file.write('1')
                else:
                    file.write('0')

        file.write('\n')
        file.write(str(len(self.entities)))
        file.write('\n')

        for ent in self.entities:
            for i in range(len(EntityClasses)):
                if type(ent)==EntityClasses[i]:
                    file.write(str(i))

            file.write('\n')
            ent.save(file)
            #file.write('\n')

    def destroy_entity(self, target):
        self.entities.remove(target)

    def add_entity(self, entity):
        self.entities.append(entity)
        if isinstance(entity, Player):
            self.players.append(entity)
            self.hud = HUD(self.players[0])

    def add_player(self, player):
        assert isinstance(player, Player)
        self.players.append(player)
        self.entities.append(player)
        self.hud = HUD(self.players[0])

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
        self.camera_pos = (self.players[0].moving_component.position[0] - CONST_CAMERA_PLAYER_OFFSET_X,
                           self.players[0].moving_component.position[1] - CONST_CAMERA_PLAYER_OFFSET_Y)

    @staticmethod
    def load(path):
        file = open(path,"r")

        level = Level()
        s = file.readline()
        c=0
        for i in range(level.col):
            for j in range(level.row):
                if int(s[c])==1:
                    level.map[j][i] = True
                else:
                    level.map[j][i] = False
                print("%d %d %d" % (int(s[c]),j,i))
                c+=1

        s = file.readline()
        ent_count = int(s)
        print(ent_count)

        for i in range(ent_count):
            s = file.readline()
            j = int(s)
            print(EntityClasses[j])
            ent = EntityClasses[j].load(file, level)
            level.add_entity(ent)

        return level
