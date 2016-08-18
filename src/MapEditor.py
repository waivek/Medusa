from src.Level import *

class MapEditor:
    def __init__(self):
        #self.file = open("tmp.lev", 'r+')
        #self.level = Level()
        self.level = Level.load(r"..\level.txt")
        self.level.show_hud = False

        if len(self.level.players) >= 1:
            self.level.camera_pos = (self.level.players[0].moving_component.position[0] - CONST_CAMERA_PLAYER_OFFSET_X,
                           self.level.players[0].moving_component.position[1] - CONST_CAMERA_PLAYER_OFFSET_Y)

        self.zoomlevel = 1

        self.selected = (-1,-1)

        self.tile_spr = Sprite(ImageEnum.BLOCK)
        self.tile_spr.set_location((0,0))

        self.ents1 = []
        self.ents1_spr = []
        self.ents1.append(Player)
        self.ents1_spr.append(Sprite(ImageEnum.PLAYER1_JUMPRIGHT))
        self.ents1.append(Skeleton)
        self.ents1_spr.append(Sprite(ImageEnum.SKELETON_STANDING))

        self.ents2 = []
        self.ents2_spr = []
        self.ents2.append(RegenPowerup)
        self.ents2_spr.append(Sprite(ImageEnum.POWERUP_BLUE))
        self.ents2.append(StaminaPowerup)
        self.ents2_spr.append(Sprite(ImageEnum.POWERUP_GREEN))
        self.ents2.append(HastePowerup)
        self.ents2_spr.append(Sprite(ImageEnum.POWERUP_LIGHT))
        self.ents2.append(GravityPowerup)
        self.ents2_spr.append(Sprite(ImageEnum.POWERUP_PURPLE))
        self.ents2.append(BouncePowerup)
        self.ents2_spr.append(Sprite(ImageEnum.POWERUP_DARK))

        for i in range(len(self.ents1_spr)):
            self.ents1_spr[i].set_location((i*32,32))

        for i in range(len(self.ents2_spr)):
            self.ents2_spr[i].set_location((i*32,64))

        self.key_spr = []
        for i in range(KeyEnum.NUM.value):
            self.key_spr.append(Sprite(KeySprites[i]))
            self.key_spr[len(self.key_spr) - 1].set_location((i*32,96))

        self.lock_spr = []
        for i in range(KeyEnum.NUM.value):
            self.lock_spr.append(Sprite(LockSprites[i]))
            self.lock_spr[len(self.lock_spr) - 1].set_location((i * 32, 128))

        self.weapon_spr = []
        for i in range(WeaponEnum.NUM.value):
            self.weapon_spr.append(Sprite(WeaponSprites[i]))
            self.weapon_spr[len(self.weapon_spr) - 1].set_location((i * 32, 160))

        self.ammo_spr = []
        for i in range(WeaponEnum.NUM.value):
            self.ammo_spr.append(Sprite(AmmoSprites[i]))
            self.ammo_spr[len(self.ammo_spr) - 1].set_location((i * 32, 192))

    def draw(self, screen):
        self.level.draw(screen)

        self.tile_spr.draw(screen,(0,0))

        for i in self.ents1_spr:
            i.draw(screen,(0,0))

        for i in self.ents2_spr:
            i.draw(screen,(0,0))

        for i in self.key_spr:
            i.draw(screen,(0,0))

        for i in self.lock_spr:
            i.draw(screen,(0,0))

        for i in self.weapon_spr:
            i.draw(screen,(0,0))

        for i in self.ammo_spr:
            i.draw(screen,(0,0))

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.level.save_data(r"..\level.txt")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mpos = pygame.mouse.get_pos()
                flag = 0
                #print(mpos)

                if src.Util.point_in_rect(mpos, self.tile_spr.sprite_rect()):
                    self.selected = (4,0)
                    flag = 1

                for i in range(len(self.ents1_spr)):
                    if src.Util.point_in_rect(mpos, self.ents1_spr[i].sprite_rect()):
                        self.selected = (0, i)
                        flag = 1

                for i in range(len(self.ents2_spr)):
                    if src.Util.point_in_rect(mpos, self.ents2_spr[i].sprite_rect()):
                        self.selected = (1, i)
                        flag = 1

                for i in range(len(self.key_spr)):
                    if src.Util.point_in_rect(mpos, self.key_spr[i].sprite_rect()):
                        self.selected = (2, i)
                        flag = 1

                for i in range(len(self.lock_spr)):
                    if src.Util.point_in_rect(mpos, self.lock_spr[i].sprite_rect()):
                        self.selected = (3, i)
                        flag = 1

                for i in range(len(self.weapon_spr)):
                    if src.Util.point_in_rect(mpos, self.weapon_spr[i].sprite_rect()):
                        self.selected = (5, i)
                        flag = 1

                for i in range(len(self.ammo_spr)):
                    if src.Util.point_in_rect(mpos, self.ammo_spr[i].sprite_rect()):
                        self.selected = (6, i)
                        flag = 1

                print(self.selected)
                if(flag==0):
                    worldpos = (mpos[0]+self.level.camera_pos[0],mpos[1]+self.level.camera_pos[1])
                    cell = (int(worldpos[0]/BLOCK_SIZE),int(worldpos[1]/BLOCK_SIZE))

                    if self.selected[0]==0:
                        e = self.ents1[self.selected[1]]((cell[0]*BLOCK_SIZE, cell[1]*BLOCK_SIZE), self.level)
                        self.level.add_entity(e)

                    if self.selected[0]==1:
                        e = self.ents2[self.selected[1]]((cell[0]*BLOCK_SIZE, cell[1]*BLOCK_SIZE))
                        self.level.add_entity(e)

                    if self.selected[0]==2:
                        e = Key(KeyEnum(self.selected[1]), (cell[0]*BLOCK_SIZE,cell[1]*BLOCK_SIZE))
                        self.level.add_entity(e)

                    if self.selected[0]==3:
                        e = Lock(KeyEnum(self.selected[1]), (cell[0]*BLOCK_SIZE,cell[1]*BLOCK_SIZE))
                        self.level.add_entity(e)

                    if self.selected[0]==5:
                        e = WeaponItem(WeaponEnum(self.selected[1]), (cell[0]*BLOCK_SIZE,cell[1]*BLOCK_SIZE))
                        self.level.add_entity(e)

                    if self.selected[0]==6:
                        e = Ammo(WeaponEnum(self.selected[1]), (cell[0]*BLOCK_SIZE,cell[1]*BLOCK_SIZE))
                        self.level.add_entity(e)

            #zoom
            if event.button == 4:
                self.zoomlevel -= 1
                if self.zoomlevel < 1:
                    self.zoomlevel = 1

            if event.button == 5:
                self.zoomlevel += 1
                if self.zoomlevel > 5:
                    self.zoomlevel = 5


    def update(self, deltatime):
        deltatime /= 1000
        speed = 500
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.level.camera_pos = (self.level.camera_pos[0] - speed*deltatime, self.level.camera_pos[1])

        if keys[pygame.K_RIGHT]:
            self.level.camera_pos = (self.level.camera_pos[0] + speed*deltatime, self.level.camera_pos[1])

        if keys[pygame.K_UP]:
            self.level.camera_pos = (self.level.camera_pos[0], self.level.camera_pos[1] - speed*deltatime)

        if keys[pygame.K_DOWN]:
            self.level.camera_pos = (self.level.camera_pos[0], self.level.camera_pos[1] + speed*deltatime)

        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            if self.selected[0] == 4:
                mpos = pygame.mouse.get_pos()
                worldpos = (mpos[0] + self.level.camera_pos[0], mpos[1] + self.level.camera_pos[1])
                cell = (int(worldpos[0] / BLOCK_SIZE), int(worldpos[1] / BLOCK_SIZE))
                self.level.tiles[cell[1]][cell[0]] = True

        if mouse[2]:
            mpos = pygame.mouse.get_pos()
            worldpos = (mpos[0] + self.level.camera_pos[0], mpos[1] + self.level.camera_pos[1])
            cell = (int(worldpos[0] / BLOCK_SIZE), int(worldpos[1] / BLOCK_SIZE))

            if self.level.tiles[cell[1]][cell[0]]:
                self.level.tiles[cell[1]][cell[0]] = False

            for e in self.level.entities:
                if src.Util.point_in_rect(worldpos, e.sprite.sprite_rect()):
                    self.level.entities.remove(e)