

BLOCK_SIZE = 32
class Level():
    def __init__(self, row, col):
        self.player1 = None
        self.player2 = None
        self.row = row
        self.col = col
        self.my_list = \
            [
                [ y >= (self.row / 2) for x in range(self.col)]
                for y in range(self.row)
            ]

    def add_player(self, player):
        if self.player1 == None:
            pass
            # do player1 code
        elif self.player2 == None:
            pass
            # do player2 code
        else:
            pass
            # ERROR


l = Level(6, 3)
