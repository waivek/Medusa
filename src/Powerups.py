from src.Powerup import *
from src.LoadResources import *
from src.Buff import *

CONST_REGEN_HEAL_RATE = 100

class StaminaPowerup(Powerup):
    def __init__(self,pos):
        super().__init__(ImageEnum.POWERUP_GREEN, 32, pos)

        def buff_func(player, buff):
            player.energy_regain_rate /= 3
            player.sprint_energy_rate *= 2

        b = Buff(buff_func, 5000)

        self.buff = b

class RegenPowerup(Powerup):
    def __init__(self,pos):
        super().__init__(ImageEnum.POWERUP_BLUE, 32, pos)

        def buff_func(player, buff):
            if buff.timer.get_time() >= CONST_REGEN_HEAL_RATE:
                player.health.health += 1

                if (buff.duration > CONST_REGEN_HEAL_RATE):
                    player.buffs.append(Buff(buff_func, buff.duration - CONST_REGEN_HEAL_RATE))
                player.buffs.remove(buff)

        b = Buff(buff_func, 600)

        self.buff = b

class SpringPowerup(Powerup):
    def __init__(self,pos):
        super().__init__(ImageEnum.POWERUP_DARK, 32, pos)

        def buff_func(player, buff):
            player.jump_velocity *= 1.5

        buff = Buff(buff_func, 5000)

        self.buff = buff

class HastePowerup(Powerup):
    def __init__(self,pos):
        super().__init__(ImageEnum.POWERUP_LIGHT, 32, pos)

        def buff_func(player, buff):
            player.speed *= 1.25
            player.sprint_speed *= 1.5

        buff = Buff(buff_func, 5000)

        self.buff = buff

class GravityPowerup(Powerup):
    def __init__(self,pos):
        super().__init__(ImageEnum.POWERUP_PURPLE, 32, pos)

        def buff_func(player, buff):
            player.gravity /= 3

        buff = Buff(buff_func, 5000)

        self.buff = buff