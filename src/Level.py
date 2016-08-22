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
    WEAPON = 9
    AMMO = 10

EntityClasses = [Player,Skeleton,RegenPowerup,HastePowerup,StaminaPowerup,GravityPowerup,BouncePowerup,Key,Lock,WeaponItem,Ammo]

class Level:
    def __init__(self):
        self.row = 100
        self.col = 100
        self.tiles = \
            [
                [y >= (10) for x in range(self.col)]
                for y in range(self.row)
                ]

        self.sky_sprite = Sprite(ImageEnum.SKY)
        self.sky_sprite.bounds = (0,0,2000,2000)

        self.block_sprite = Sprite(ImageEnum.BLOCK)
        self.camera_pos = (32*10, 0)

        self.monsters = []
        self.players = []
        self.entities = []

        self.colliders = []

        for i in range(self.col):
            self.tiles[0][i] = True
            self.tiles[i][0] = True
            self.tiles[99][i] = True
            self.tiles[i][99] = True

        self.hud = None
        self.show_hud = True

    def save_data(self, path):
        print("saving")
        file = open(path, 'r+')
        for i in range(self.col):
            for j in range(self.row):
                if self.tiles[j][i]:
                    file.write('1')
                else:
                    file.write('0')

        file.write('\n')
        file.write(str(len(self.entities)))
        file.write('\n')

        for ent in self.players:
            for i in range(len(EntityClasses)):
                if type(ent)==EntityClasses[i]:
                    file.write(str(i))

            file.write('\n')
            ent.save(file)

        for ent in self.entities:
            if type(ent)!=Player:
                for i in range(len(EntityClasses)):
                    if type(ent)==EntityClasses[i]:
                        file.write(str(i))

                file.write('\n')
                ent.save(file)

    def destroy_entity(self, target):
        if target in self.entities:
            self.entities.remove(target)
        if target in self.colliders:
            self.colliders.remove(target)

    def add_entity(self, entity):
        self.entities.append(entity)
        if isinstance(entity, Player):
            self.players.append(entity)
            self.hud = HUD(self.players[0])

        if isinstance(entity, Skeleton) or isinstance(entity, Lock):
            self.colliders.append(entity)

    def draw(self, screen):
        self.sky_sprite.draw(screen, (0,0))

        for i in range(self.row):
            for j in range(self.col):
                if self.tiles[i][j] is True:
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

    def point_in_wall(self, p):
        cx = int(p[0]/32)
        cy = int(p[1]/32)

        if cx > self.col or cy > self.row:
            #print("out of bounds")
            return 1

        if self.tiles[cy][cx]:
            #print("colliding with %d %d" % (cy, cx))
            return 1
        return 0

    # def point_in_wall(self, x, y):
    #     for i in range(self.col):
    #         for j in range(self.row):
    #             if self.tiles[j][i]:
    #                 tile_rect = pygame.Rect(BLOCK_SIZE * i, BLOCK_SIZE * j, BLOCK_SIZE, BLOCK_SIZE)
    #                 if tile_rect.collidepoint(x,y):
    #                     return True
    #     return False

    def point_in_collider(self, p, colliders):
        for collider in colliders:
            if collider.sprite.sprite_rect().collidepoint(p):
                return True
        return False

    def update(self, deltatime):
        #update entities and detect collision
        for entity in self.entities:
            entity.update(deltatime)

        self.hud.update(deltatime)

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
                    level.tiles[j][i] = True
                else:
                    level.tiles[j][i] = False
                #print("%d %d %d" % (int(s[c]),j,i))
                c+=1

        s = file.readline()
        ent_count = int(s)
        #print(ent_count)

        for i in range(ent_count):
            s = file.readline()
            if s == '\n':
                continue
            j = int(s)
            #print(EntityClasses[j])
            ent = EntityClasses[j].load(file, level)
            level.add_entity(ent)

        return level
