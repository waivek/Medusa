from src.Ammo import *
from src.Projectile import *

WeaponFunctions = []

class WeaponEquipped:
    def __init__(self, weapon_type, ammo, owner):
        self.weapon_type = weapon_type
        self.ammo = ammo
        self.sprite = Sprite(WeaponSprites[weapon_type.value])
        self.owner = owner
        self.collision_component = CollisionComponent(self, self.owner.level)

        self.is_attacking = False

        self.weapon_attach = (16,18)

        self.attach_points = []

    def use(self, mousepos):
        WeaponFunctions[self.weapon_type.value](self, mousepos)

    def update_sprite(self):
        # old_rect = self.sprite.sprite_rec
        self.sprite.sprite = gImages[self.sprite.sprite_enum.value]
        # surface = pygame.Surface((2 * self.weapon_attach[0], 2 * self.weapon_attach[1]),pygame.SRCALPHA)
        # surface.fill((0,0,0,0))
        # self.sprite.draw(surface, (0,0))
        # surface.blit(self.sprite.sprite,(0,0,2 * self.weapon_attach[0], 2 * self.weapon_attach[1]))
        # self.sprite.sprite = surface
        self.sprite.sprite_rec = pygame.Rect(0, 0, 2 * self.weapon_attach[0], 2 * self.weapon_attach[1])
        self.sprite.set_location((self.owner.sprite.sprite_rect().topleft[0] - self.weapon_attach[0]
                                  + self.attach_points[self.owner.sprite.state][self.owner.sprite.get_frame()][0],
                                  self.owner.sprite.sprite_rect().topleft[1] - self.weapon_attach[1]
                                  + self.attach_points[self.owner.sprite.state][self.owner.sprite.get_frame()][1]))
        print(self.sprite.sprite_rec)
        # print(self.sprite.sprite_rec.topleft)
        # print(self.owner.sprite.sprite_rect().topleft)
        self.sprite.rotate_around_point(self.attach_points[self.owner.sprite.state][self.owner.sprite.get_frame()][2],
                                        (self.weapon_attach[0], self.weapon_attach[1]))
        print(self.sprite.sprite_rec)

        if self.owner.facing == Facing.RIGHT:
            self.sprite.set_flipped(True)
        else:
            self.sprite.set_flipped(False)

    def draw(self,screen,camera):
        self.update_sprite()
        self.sprite.draw(screen, camera)

    def update(self, deltatime):
        #self.sprite.update(deltatime)
        self.sprite.set_location(self.owner.moving_component.position)
        self.update_sprite()

        if self.owner.is_attacking:
            collider = self.collision_component.check_collisions()
            print("checking collisions")
            if collider is not None:
                print(collider)
                if collider is not self.owner:
                    print("colliding")
                    from src.Skeleton import Skeleton
                    if isinstance(collider, Skeleton):
                        collider.health -= 1



def init_weapons():

    def passfunc(projectile):
        pass

    def arrowinit(projectile):
        play_sound(SoundEnum.ARROW_SHOOT)
        projectile.moving_component.gravity = 100
        projectile.moving_component.collision_bounds = pygame.Rect(1,11,30,11)

    def arrowupd(projectile):
        if projectile.moving_component.velocity == (0,0):
            projectile.owner.level.destroy_entity(projectile)

    def dealdmg(projectile, other):
        print("collision called")
        from src.Skeleton import Skeleton
        if isinstance(other, Skeleton):
            other.health -= 1
            projectile.owner.level.destroy_entity(projectile)
        else:
            projectile.owner.level.destroy_entity(projectile)

    def bow(weapon, target):
        if weapon.ammo > 0:
            weapon.ammo -= 1
            vel = pygame.math.Vector2(500, 0)
            rot = math.atan2((target[1] - weapon.owner.moving_component.position[1])-16
                                 ,(target[0] - weapon.owner.moving_component.position[0])-16)
            vel = vel.rotate(math.degrees(rot))
            vel2 = (vel.x,vel.y)
            p = Projectile(AmmoSprites[weapon.weapon_type.value], weapon.owner, weapon.owner.moving_component.position, vel2,
                           arrowinit,arrowupd,dealdmg)
            weapon.owner.level.add_entity(p)
    WeaponFunctions.append(bow)

    def sword(weapon, target):
        from src.Player import PlayerAnimState
        weapon.is_attacking = True
        if weapon.owner.facing == Facing.LEFT:
            weapon.owner.sprite.set_state(PlayerAnimState.STAB_LEFT)
        else:
            weapon.owner.sprite.set_state(PlayerAnimState.STAB_RIGHT)
    WeaponFunctions.append(sword)