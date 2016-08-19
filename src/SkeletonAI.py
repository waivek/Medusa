from enum import Enum
from src.WorldConstants import *
import src.Util
from src.Line import *

class SkeletonAIEnum(Enum):
    PATROL = 0
    AGGRO = 1
    CHASING_PLAYER = 2

class SkeletonAI:
    def __init__(self, obj):
        self.obj = obj
        self.level = obj.level
        self.player = self.level.players[0]

        self.state = SkeletonAIEnum.PATROL

        self.last_known_player_pos = None

    def update(self, deltatime):
        my_center = self.obj.sprite.get_center()
        player_center = self.player.sprite.get_center()
        line = Line(my_center[0],my_center[1],player_center[0],player_center[1])

        colliders = list(self.level.colliders)
        colliders.remove(self.obj)

        if line.check_collision(self.level,BLOCK_SIZE,colliders) == False:
            self.last_known_player_pos = player_center

        if self.last_known_player_pos is not None:
            self.state = SkeletonAIEnum.AGGRO
            print(self.state)
        else:
            self.state = SkeletonAIEnum.PATROL

        if self.state == SkeletonAIEnum.PATROL:
            pos = my_center
            if self.obj.facing == Facing.LEFT:
                pos = (pos[0]-BLOCK_SIZE,pos[1])
            else:
                pos = (pos[0]+BLOCK_SIZE,pos[1])

            if self.level.point_in_wall(pos) \
                or (not self.level.point_in_wall((pos[0],pos[1]+BLOCK_SIZE)))\
                or self.level.point_in_collider(pos, colliders):
                self.obj.move_direction(src.Util.turn_around(self.obj.facing))
            else:
                self.obj.move_direction(self.obj.facing)

        elif self.state == SkeletonAIEnum.AGGRO:
            if abs(self.last_known_player_pos[0]-my_center[0]) < 50:
                self.obj.stand_still()
                self.obj.attack()
            elif self.last_known_player_pos[0] < my_center[0]:
                self.obj.move_direction(Facing.LEFT)
            else:
                self.obj.move_direction(Facing.RIGHT)