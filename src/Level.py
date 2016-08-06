from src.Sprite import Sprite

BLOCK_SIZE = 32
class Level():
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
        print(self.map)
        self.sky_sprite = Sprite("..\\raw\\sky.png")
        self.block_spr = Sprite("..\\raw\\tile.jpg")

    def add_player(self, player):
        if self.player1 == None:
            self.player1 = player
        elif self.player2 == None:
            self.player2 = player
        else:
            raise Exception("Tried to add player>2")

    def draw(self, screen):
        self.sky_sprite.draw(screen)

        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] == True:
                    self.block_spr.set_location((BLOCK_SIZE*j,BLOCK_SIZE*i))
                    self.block_spr.draw(screen)

        if self.player1 is not None:
            self.player1.draw(screen)
        if self.player2 is not None:
            self.player2.draw(screen)

    def handle_event(self, event):
        if self.player1 is not None:
            self.player1.handleEvent(event)
        if self.player2 is not None:
            self.player2.handleEvent(event)

    def Update(self, deltaTime):
        if self.player1 is not None:
            self.player1.Update(deltaTime)
        if self.player2 is not None:
            self.player2.draw()
            self.player2.Update(deltaTime)
            pass
            # do player1 code
        elif self.player2 == None:
            pass
            # do player2 code
        else:
            pass
            # ERROR


l = Level(6, 3)
