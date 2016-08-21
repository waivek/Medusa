class Health:
    def __init__(self, health, cooldown_seconds):
        from src.Timer import Timer
        self.health = health
        self.cooldown_seconds = cooldown_seconds
        self.time_elapsed_since_hit = self.cooldown_seconds
        self.timer = Timer()

    def deal_damage(self, damage):
        t = self.timer.get_time()
        if t > self.cooldown_seconds * 1000:
            self.health = self.health - damage
            self.time_elapsed_since_hit = 0
            self.timer.reset()