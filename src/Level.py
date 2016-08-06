from src.Sprite import Sprite
from src.Sprite import rect_intersect
from src.Player import PlayerState
from src.Player import BLOCK_SIZE
from src.LoadResources import ImageEnum
from src.LoadResources import gImages
import pygame

class Level:
    def __init__(self, row, col):
        self.player1 = None
        self.player2 = None
        self.row = row
        self.col = col
        self.map = \
            [
                [ y >= (self.row / 2) for x in range(self.col)]
                for y in range(self.row)
            ]

        self.sky_sprite = Sprite(ImageEnum.SKY)
        self.block_sprite = Sprite(ImageEnum.BLOCK)

    def add_player(self, player):
        if self.player1 is None:
            self.player1 = player
        elif self.player2 is None:
            self.player2 = player
        else:
            raise Exception("Tried to add player>2")

    def draw(self, screen):
        self.sky_sprite.draw(screen)

        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] is True:
                    self.block_sprite.set_location((BLOCK_SIZE*j,BLOCK_SIZE*i))
                    self.block_sprite.draw(screen)

        if self.player1 is not None:
            self.player1.draw(screen)
        if self.player2 is not None:
            self.player2.draw(screen)

    def handle_event(self, event):
        if self.player1 is not None:
            self.player1.handle_event(event)
        if self.player2 is not None:
            self.player2.handle_event(event)

    def update(self, deltatime):
        if self.player1 is not None:
            self.player1.update(deltatime)
            for i in range(self.col):
                for j in range(self.row):
                    if self.map[j][i]:
                        tilerect = pygame.Rect(BLOCK_SIZE*i,BLOCK_SIZE*j,BLOCK_SIZE,BLOCK_SIZE)
                        if rect_intersect(self.player1.getrekt(), tilerect):
                            self.player1.state = PlayerState.GROUND

        if self.player2 is not None:
            self.player2.update(deltatime)
