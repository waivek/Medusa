from enum import Enum
from src.WorldConstants import *
import src.Util

class SkeletonAIEnum(Enum):
    MOVING = 0
    ATTACKING = 1
    CHASING_PLAYER = 2

class SkeletonAI:
    def __init__(self, obj):
        self.obj = obj
        self.level = obj.level
        self.player = self.level.players[0]

        self.state = SkeletonAIEnum.MOVING

    def update(self, deltatime):
        if self.state == SkeletonAIEnum.MOVING:
            center = self.obj.sprite.get_center()
            pos = center
            if self.obj.facing == Facing.LEFT:
                pos = (pos[0]-BLOCK_SIZE,pos[1])
            else:
                pos = (pos[0]+BLOCK_SIZE,pos[1])

            if self.level.point_in_wall(pos) \
                or (not self.level.point_in_wall((pos[0],pos[1]+BLOCK_SIZE)))\
                or self.level.point_in_collider(pos):
                self.obj.move_direction(src.Util.turn_around(self.obj.facing))
            else:
                self.obj.move_direction(self.obj.facing)