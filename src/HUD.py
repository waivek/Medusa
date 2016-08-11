from src.LoadResources import *
from src.Player import *
from src.Sprite import *

class HUD:
    def __init__(self, player):
        self.player = player
        self.life_spr = Sprite(ImageEnum.HUD_LIFE)
        self.energy_spr = Sprite(ImageEnum.HUD_ENERGY)

    def draw(self, screen):
        self.life_spr.set_location((0, 0))
        for i in range(self.player.life):
            self.life_spr.draw(screen,(0,0))
            self.life_spr.move((32,0))

        self.energy_spr.set_location((0, 32))
        for i in range(self.player.life):
            self.energy_spr.draw(screen,(0,0))
            self.energy_spr.move((32,0))