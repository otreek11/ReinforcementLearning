from point import Point
from random import randint
from globals import *

class Obstacle(Point):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.__initial_startpos = Point(x, y)

    def next(self) -> "Obstacle":
        speed = randint(1, 3)
        pos = Obstacle(self.col, self.row + speed)
        if pos.row >= MAP_HEIGHT: pos.row = self.__initial_startpos
        return pos
    
    def do_next(self, next: "Obstacle") -> None:
        self += next

    def reset(self):
        self.row = self.__initial_startpos.row
        self.col = self.__initial_startpos.col

    def __Point__(self) -> Point:
        return Point(self.col, self.row)