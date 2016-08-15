class Line:
    def __init__(self, x1, y1, x2, y2):
        self.m = (y2 - y1) / (x2 - x1)
        self.c = y1 - (self.m * x1)

    def get_y(self, x1):
        y1 = (self.m * x1) + self.c
        return y1

    def get_x(self, y1):
        x1 = (y1 - self.c) / self.m
        return x1