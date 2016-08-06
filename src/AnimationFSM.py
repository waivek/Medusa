from src.AnimatedSprite import AnimatedSprite
from src.LoadResources import gImages
from src.LoadResources import ImageEnum

class AnimationFSM:
    def __init__(self):
        self.state = 0
        self.sprites = []

    def add_sprite(self, sprite):
        assert(isinstance(sprite,AnimatedSprite))
        self.sprites.append(sprite)

    def draw(self, screen):
        self.sprites[self.state].draw(screen)

    def update(self, deltatime):
        self.sprites[self.state].update(deltatime)
        print(self.state)

    def set_state(self, state):
        if(self.state!=state):
            self.state = state
            self.sprites[self.state].reset()

    def move(self,displacement):
        for i in range(len(self.sprites)):
            self.sprites[i].move(displacement)