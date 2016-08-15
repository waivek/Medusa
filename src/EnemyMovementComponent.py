from src.MovingComponent import MovingComponent
import src.Util

class EnemyMovementComponent:
    def __init__(self, moving_component, level):
        assert(isinstance(moving_component, MovingComponent))
        self.moving_component = moving_component
        self.initial_position_x = moving_component.position[0]
        self.RANGE = 200
        self.VELOCITY = 100
        self.moving_component.velocity = (self.VELOCITY, self.moving_component.velocity[0])
        self.distance_covered = 0
        self.level = level

    def update(self, deltaTime):
        current_position_x = self.moving_component.position[0]
        d_x = current_position_x - self.initial_position_x
        if abs(d_x) >= 500:
            self.moving_component.velocity = (-self.moving_component.velocity[0], self.moving_component.velocity[1])

        cell = src.Util.pixel2cell(self.moving_component.position[0]+16,self.moving_component.position[1]+16)
        print(cell)
        if self.moving_component.velocity[0] < 0:
            if self.level.tiles[cell[1]-1][cell[0]]:
                self.moving_component.velocity = (-self.moving_component.velocity[0], self.moving_component.velocity[1])
            #elif self.level.tiles[cell[1]-1][cell[0]+1] == False:
            #    self.moving_component.velocity = (-self.moving_component.velocity[0], self.moving_component.velocity[1])
        elif self.moving_component.velocity[0] > 0:
            if self.level.tiles[cell[1]+1][cell[0]]:
                self.moving_component.velocity = (-self.moving_component.velocity[0], self.moving_component.velocity[1])
            #elif self.level.tiles[cell[1]+1][cell[0]+1] == False:
            #    self.moving_component.velocity = (-self.moving_component.velocity[0], self.moving_component.velocity[1])
