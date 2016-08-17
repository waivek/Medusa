from src.WorldConstants import *
import src.Util
import pygame

class BlockCollision:
    def __init__(self, pos, level):
        self.x = pos[0]
        self.y = pos[1]
        self.level = level

class MovingComponent:
    def __init__(self, obj, level):
        self.obj = obj
        self.level = level

        self.position = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0,0)
        self.sprite = obj.sprite
        self.size = (BLOCK_SIZE, BLOCK_SIZE)

        self.tiles = level.tiles
        self.tiles_col = level.col
        self.tiles_row = level.row

        self.in_air = False
        self.gravity = CONST_GRAVITY

        self.collides = True
        self.collision_bounds = pygame.Rect(1,1,30,30)
        self.bounciness = 0

        def passfunc(obj1, obj2):
            pass

        self.on_collision = passfunc

    def point_in_wall(self, x, y):
        cx = int(x/32)
        cy = int(y/32)

        if cx > self.tiles_col or cy > self.tiles_row:
            #print("out of bounds")
            return 1

        if self.tiles[cy][cx]:
            #print("colliding with %d %d" % (cy, cx))
            return 1
        return 0

    def push_out_colliders(self, colliders):
        m = 0
        flag = 0
        factor = 1
        from src.Projectile import Projectile

        if isinstance(self.obj,Projectile):
            print(colliders)

        colliding_obj = None
        while flag == 0:
            my_sprite = self.sprite.sprite_rect()
            for i in range(2 * m + 2):
                if flag == 1:
                    break
                for j in range(2 * m + 2):
                    if flag==1:
                        break

                    d = (factor * (int(i / 2) * ((-1) ** (i % 2))), factor * (int(j / 2) * ((-1) ** (j % 2))))

                    #if d[0] is not m and d[1] is not m:
                    #    continue

                    b = False
                    b = b or self.point_in_wall(self.sprite.sprite_rect().topleft[0] + d[0] + self.collision_bounds[0],
                                                self.sprite.sprite_rect().topleft[1] + d[1] + self.collision_bounds[1])
                    if b and colliding_obj is None:
                        #print("setting block collider")
                        colliding_obj = BlockCollision(src.Util.pixel2cell(self.sprite.sprite_rect().topleft[0] + d[0] + self.collision_bounds[0],
                                                self.sprite.sprite_rect().topleft[1] + d[1] + self.collision_bounds[1]), self.level)

                    b = b or self.point_in_wall(self.sprite.sprite_rect().topleft[0] + d[0]
                                                + self.collision_bounds[0] + self.collision_bounds[2],
                                                self.sprite.sprite_rect().topleft[1] + d[1] + self.collision_bounds[1])

                    if b and colliding_obj is None:
                        #("setting block collider")
                        colliding_obj = BlockCollision(src.Util.pixel2cell(self.sprite.sprite_rect().topleft[0] + d[0]
                                                + self.collision_bounds[0] + self.collision_bounds[2],
                                                self.sprite.sprite_rect().topleft[1] + d[1] + self.collision_bounds[1]), self.level)

                    b = b or self.point_in_wall(self.sprite.sprite_rect().topleft[0] + d[0] + self.collision_bounds[0],
                                                self.sprite.sprite_rect().topleft[1] + d[1]
                                                + self.collision_bounds[1] + self.collision_bounds[3])

                    if b and colliding_obj is None:
                        #print("setting block collider")
                        colliding_obj = BlockCollision(src.Util.pixel2cell(self.sprite.sprite_rect().topleft[0] + d[0] + self.collision_bounds[0],
                                                self.sprite.sprite_rect().topleft[1] + d[1]
                                                + self.collision_bounds[1] + self.collision_bounds[3]), self.level)

                    b = b or self.point_in_wall(self.sprite.sprite_rect().topleft[0] + d[0]
                                                + self.collision_bounds[0] + self.collision_bounds[2],
                                                self.sprite.sprite_rect().topleft[1] + d[1]
                                                + self.collision_bounds[1] + self.collision_bounds[3])

                    if b and colliding_obj is None:
                        #print("setting block collider")
                        colliding_obj = BlockCollision(src.Util.pixel2cell(self.sprite.sprite_rect().topleft[0] + d[0]
                                                + self.collision_bounds[0] + self.collision_bounds[2],
                                                self.sprite.sprite_rect().topleft[1] + d[1]
                                                + self.collision_bounds[1] + self.collision_bounds[3]), self.level)

                    if b == False:
                        for k in range(len(colliders)):
                            new_rect = pygame.Rect(my_sprite.topleft[0]+d[0]+self.collision_bounds[0],
                                                   my_sprite.topleft[1]+d[1]+self.collision_bounds[1],
                                                   self.collision_bounds[2], self.collision_bounds[3])
                            b = b or new_rect.colliderect(colliders[k].sprite.sprite_rect())
                            #b = b or src.Util.rect_intersect(new_rect, colliders[k].sprite.sprite_rect())
                            if b:
                                from src.Projectile import Projectile
                                if type(self.obj)==Projectile:
                                    print("colliding:")
                                    print(self.obj)
                                    print(colliders[k])
                                if colliding_obj is None:
                                    print("setting collider")
                                    colliding_obj = colliders[k]
                                break

                    from src.Skeleton import Skeleton

                    if b == False:
                        self.move(d)
                        flag = 1
                        debug = 0
                        if (d[0] != 0):
                            self.velocity = (-self.velocity[0] * self.bounciness, self.velocity[1])
                            if type(self.obj)==Skeleton:
                                print("set vel")
                                print("p1")
                                print(colliding_obj)
                            debug = 1
                            assert m > 0
                            assert colliding_obj is not None

                        if (d[1] != 0):
                            self.velocity = (self.velocity[0], -self.velocity[1] * self.bounciness)
                            #print("set vel")
                            assert m > 0
                            assert colliding_obj is not None

                        assert colliding_obj is not None or m == 0
                        if debug>0:
                            if type(self.obj) == Skeleton:
                                print("p2")
                                print(colliding_obj)
                        if colliding_obj is not None:
                            self.on_collision(self.obj, colliding_obj)
                            if debug > 0 and type(self.obj)==Skeleton:
                                print("called collision")
                        elif debug > 0 and type(self.obj)==Skeleton:
                            print("not called collision")
                        break

            m += int(m/10) + 1

    def snap_out(self):
        m = 0
        flag = 0
        factor = 1
        while flag==0:
            for i in range(2*m+1):
                if flag==1:
                    break
                for j in range(2*m+1):
                    d = (factor*(int(i/2)*((-1)**(i%2))),factor*(int(j/2)*((-1)**(j%2))))

                    #if d[0] is not m and d[1] is not m:
                    #    continue

                    b = False
                    b = b or self.point_in_wall(self.sprite.sprite_rect().topleft[0] + d[0] +1,self.sprite.sprite_rect().topleft[1] + d[1] +1)
                    b = b or self.point_in_wall(self.sprite.sprite_rect().topright[0] + d[0] -1,self.sprite.sprite_rect().topright[1] + d[1] +1)
                    b = b or self.point_in_wall(self.sprite.sprite_rect().bottomleft[0] + d[0] +1,self.sprite.sprite_rect().bottomleft[1] + d[1] -1)
                    b = b or self.point_in_wall(self.sprite.sprite_rect().bottomright[0] + d[0] -1,self.sprite.sprite_rect().bottomright[1] + d[1] -1)

                    if b == False:
                        self.move(d)
                        if (d[0] != 0):
                            self.velocity = (-self.velocity[0]*self.bounciness, self.velocity[1])
                        if (d[1] != 0):
                            self.velocity = (self.velocity[0], -self.velocity[1]*self.bounciness)
                        #print(m)
                        flag=1
                        break
            m += 1

    def move(self, displacement):
        self.sprite.move(displacement)
        newx = self.position[0] + int(displacement[0])
        newy = self.position[1] + int(displacement[1])
        self.position = (newx, newy)

    def update_position(self, displacement):
        from src.Player import Player
        from src.Projectile import Projectile
        old_pos = self.position

        #update position
        self.move(displacement)

        #check for collisions
        if self.collides:
            #self.snap_out()
            #if isinstance(self.obj, Player) or isinstance(self.obj, Projectile):
            #    copy = list(self.level.colliders)
            #    self.push_out_colliders(copy)

            bounds = (32,32)

            vel_rect = None
            if displacement[0] >= 0:
                if displacement[1] >= 0:
                    vel_rect = pygame.Rect(old_pos[0], old_pos[1],
                                           displacement[0]+bounds[0], displacement[1]+bounds[1])
                else:
                    vel_rect = pygame.Rect(old_pos[0], old_pos[1] + bounds[1],
                                           displacement[0],
                                           displacement[1] + bounds[1])
            else:
                if displacement[1] >= 0:
                    vel_rect = pygame.Rect(old_pos[0]+ bounds[0], old_pos[1],
                                           displacement[0], displacement[1]+bounds[1])
                else:
                    vel_rect = pygame.Rect(old_pos[0]+ bounds[0], old_pos[1] + bounds[1],
                                           displacement[0],
                                           displacement[1])

            copy = []
            #if isinstance(self.obj, Player) or isinstance(self.obj, Projectile):
            for ent in self.level.colliders:
                if ent is not self.obj:
                    #if vel_rect.colliderect(ent.sprite.sprite_rect()):
                    copy.append(ent)
            self.push_out_colliders(copy)

        #check if falling
        if old_pos[1]==self.position[1]:
            self.in_air = False
        else:
            self.in_air = True

    def update_velocity(self, acceleration):
        newx = self.velocity[0] + acceleration[0]
        newy = self.velocity[1] + acceleration[1]

        #cap the velocity
        if(newx>CONST_MAX_VELOCITY):
            newx = CONST_MAX_VELOCITY
        if(newy>CONST_MAX_VELOCITY):
            newy=CONST_MAX_VELOCITY

        self.velocity = (newx, newy)

    def update(self, deltatime):
        dt = deltatime / 1000

        # update parameters
        self.update_position((self.velocity[0] * dt, self.velocity[1] * dt))

        self.update_velocity(((self.acceleration[0] * dt, self.acceleration[1] * dt)))

        self.acceleration = (self.acceleration[0], self.gravity)
