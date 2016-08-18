from src.AnimationFSM import *
from src.WeaponEquipped import *

class EquipComponent:
    def __init__(self, obj, level):
        self.obj = obj
        self.sprite = obj.sprite
        assert isinstance(self.sprite, AnimationFSM)
        self.level = level

        self.left_hand = None
        self.right_hand = None

        self.attach_points = []
        for i in range(len(obj.sprite.sprites)):
            self.attach_points.append([])
            for j in range(obj.sprite.sprites[i].max_frames):
                self.attach_points[i].append((0,0,0))

        self.load_attach_points(r"..\raw\Sprites\player\attach.txt")

    def load_attach_points(self, filename):
        file = open(filename, "r")
        for i in range(len(self.attach_points)):
            for j in range(len(self.attach_points[i])):
                s = file.readline()
                if s=="":
                    print("ERROR: attach points not enough data")
                p = s.split()
                self.attach_points[i][j] = (int(p[0]),int(p[1]),int(p[2]))


    def print_attach_points(self):
        for i in range(len(self.attach_points)):
            for j in range(len(self.attach_points[i])):
                print(self.attach_points[i][j],end=" ")
            print("")

    def draw_right(self, screen, camera):
        if self.right_hand is not None:
            self.right_hand.draw(screen, camera)

    def draw_left(self, screen, camera):
        if self.left_hand is not None:
            self.left_hand.draw(screen, camera)

    def equip_right(self, weapon):
        assert isinstance(weapon, WeaponEquipped)
        self.right_hand = weapon
        self.right_hand.attach_points = self.attach_points

    def equip_left(self, weapon):
        assert isinstance(weapon, WeaponEquipped)
        self.left_hand = weapon
        self.left_hand.attach_points = self.attach_points
