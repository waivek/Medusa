from src.Vector2i import Vector2i
from src.AnimationFSM import AnimationFSM

class Skeleton:
    def __init__(self):
        self.position = Vector2i(_x=10, _y=0)

    def draw(self, screen):
        self.sprite.draw(screen)
        self.sprite = AnimationFSM()
