import math

class Line:
    def __init__(self, x1, y1, x2, y2):
        if x2 == x1: #prevent divide by 0!
            x2 += 1

        self.p1 = (x1, y1)
        self.p2 = (x2, y2)

        self.dy = (y2 - y1)
        self.dx = (x2 - x1)

        self.m = self.dy / self.dx
        self.c = y1 - (self.m * x1)

        self.angle = math.atan2(self.dy,self.dx)
        self.x_t = math.cos(self.angle)
        self.y_t = math.sin(self.angle)

        self.distance = math.sqrt(self.dy*self.dy + self.dx*self.dx)

    def get_y(self, x1):
        y1 = (self.m * x1) + self.c
        return y1

    def get_x(self, y1):
        x1 = (y1 - self.c) / self.m
        return x1

    def check_collision(self, level, step):
        for t in range(0, self.distance, step):
            x = self.p1[0] + self.x_t * t
            y = self.p1[1] + self.y_t * t
            if level.point_in_wall((x, y)) or level.point_in_collider((x, y)):
                return True
        return False

    def get_valid_points(self, level, step):
        points = []
        for t in range(0, int(self.distance), step):
            x = self.p1[0] + self.x_t * t
            y = self.p1[1] + self.y_t * t
            if level.point_in_wall((x, y)) or level.point_in_collider((x, y)):
                break
            points.append((x,y))
        return points