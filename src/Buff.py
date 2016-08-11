from src.Timer import *

class Buff:
    def __init__(self, func, duration):
        self.func = func
        self.duration = duration
        self.timer = Timer()
        self.is_expired = False

    def start(self):
        self.timer = Timer()

    def call_func(self, player):
        self.func(player)

    def update(self, deltatime):
        t = self.timer.get_time()
        if t > self.duration:
            self.is_expired = True