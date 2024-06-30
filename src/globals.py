from percentage import Percentage
from point import *

MAP = [
    "              ",
    "       K      ",
    "              ",
    " R         X  ",
    "              ",
    "              ",
    "              ",
    "              ",
    "              "
]

MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)

def MAP_CONTAINS(point: Point) -> bool:
    return 0 <= point.col < MAP_WIDTH and 0 <= point.row < MAP_HEIGHT

CONSTANTS = {
    'epsilon' : Percentage(5),
    'alpha' : Percentage(3),
    'gamma' : Percentage(6)
}

VALUES = {
    'reward' : 1,
    'none' : 0,
    'punishment' : -1
}

