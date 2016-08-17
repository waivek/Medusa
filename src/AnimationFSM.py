from src.AnimatedSprite import AnimatedSprite
from src.LoadResources import gImages
from src.LoadResources import ImageEnum
from enum import Enum

class AnimationFSM:
    def __init__(self):
        self.state = 0
        self.sprites = []

    def add_sprite(self, sprite):
        assert(isinstance(sprite,AnimatedSprite))
        self.sprites.append(sprite)

    def draw(self, screen, camera):
        self.sprites[self.state].draw(screen, camera)

    def update(self, deltatime):
        self.sprites[self.state].update(deltatime)

    def set_state(self, state):
        if isinstance(state, Enum):
            if(self.state!=state.value):
                self.state = state.value
                self.sprites[self.state].reset()
        else:
            if (self.state != state):
                self.state = state
                self.sprites[self.state].reset()

    def move(self,displacement):
        for i in range(len(self.sprites)):
            self.sprites[i].move(displacement)

    def full_sprite_rect(self):
        return self.sprites[self.state].full_sprite_rect()

    def sprite_rect(self):
        return self.sprites[self.state].sprite_rect()

    def get_center(self):
        return self.sprites[self.state].get_center()