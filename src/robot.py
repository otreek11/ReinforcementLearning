import random
from point import *
from obstacle import *
from globals import *
import numpy as np

class Robot(Point):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.__initial_pos = Point(x, y)

    def choose_action(self, obstacle: Obstacle, Q_MATRIX):
        valid_actions = self.get_valid_actions()
        if CONSTANTS['epsilon'].roll():
            return random.choice(valid_actions)
        return np.argmax(Q_MATRIX[self.col, self.row, obstacle.col, obstacle.row])
    
    def next(self, action: Point):
        return Robot(self.col + action.col, self.row + action.row)
    
    def do_next(self, next: "Robot"):
        self += next

    def get_valid_actions(self) -> list[Point]:
        valid = []
        directions = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1), Point(1, 1), Point(-1, 1), Point(1, -1), Point(-1, -1)]
        for direction in directions:
            new_pos = self + direction
            if MAP_CONTAINS(new_pos):
                valid.append(direction)

        return valid
    
    def reset(self):
        self.row = self.__initial_pos.row
        self.col = self.__initial_pos.col

    def act(self, action: Point):
        self += action

    def __Point__(self) -> Point:
        return Point(self.col, self.row)

