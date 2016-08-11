from src.Powerup import *
from src.LoadResources import *
from src.Buff import *
class StaminaPowerup(Powerup):
    def __init__(self,pos):
        super().__init__(ImageEnum.HUD_ENERGY, pos)

        def buff_func(player):
            player.energy_regain_rate /= 2

        buff = Buff(buff_func, 5000)

        self.buff = buff