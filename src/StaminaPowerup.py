from src.Powerup import *
from src.LoadResources import *
class StaminaPowerup(Powerup):
    def __init__(self,pos):
        super().__init__(ImageEnum.HUD_ENERGY, pos)

        def buff(player):
            player.energy_regain_rate /= 2
        self.buff = buff