from src.Powerup import *
from src.LoadResources import *
from src.Buff import *

class StaminaPowerup(Powerup):
    def __init__(self,pos):
        super().__init__(ImageEnum.POWERUP_GREEN, 32, pos)

        def buff_func(player, buff):
            player.energy_regain_rate /= 3

        b = Buff(buff_func, 5000)

        self.buff = b

class RegenPowerup(Powerup):
    def __init__(self,pos):
        super().__init__(ImageEnum.POWERUP_RED, 32, pos)

        def buff_func(player, buff):
            if buff.timer.get_time() >= 1000:
                player.health.health += 1

                if (buff.duration > 1000):
                    player.buffs.append(Buff(buff_func, buff.duration - 1000))
                player.buffs.remove(buff)

        b = Buff(buff_func, 4000)

        self.buff = b

class JumpPowerup(Powerup):
    def __init__(self,pos):
        super().__init__(ImageEnum.POWERUP_YELLOW, 32, pos)

        def buff_func(player, buff):
            player.jump_velocity *= 2

        buff = Buff(buff_func, 5000)

        self.buff = buff