class Vector2i:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def add(self, other):
        v = Vector2i(self.x+other.x,self.y+other.y)
        return v

    def negate(self, other):
        v = Vector2i(-self.x, -self.y)
        return v

    def multiply(self, c):
        v = Vector2i(c*self.x, c*self.y)
        return v

    def multiply_vector(self, other):
        v = Vector2i(self.x * other.x, self.y * other.y)
        return v