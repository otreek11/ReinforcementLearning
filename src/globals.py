from percentage import *

# K -> Obstacle
# R -> Robot
# X -> Objective

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

def MAP_CONTAINS(point: tuple) -> bool:
    return 0 <= point[0] < MAP_WIDTH and 0 <= point[1] < MAP_HEIGHT

DIRECTIONS = [ 
    (0, 0),  # stay still
    (0, 1),  # move right
    (1, 0),  # move down
    (-1, 0), # move left
    (0, -1), # move up
    (1, 1),  # move down-right
    (-1, 1), # move down-left
    (1, -1), # move up-right
    (-1, -1) # move up-left
]

EPSILON = Percentage(8)

CONSTANTS = {
    'alpha': 0.04,
    'gamma': 0.7
}

REWARDS = {
    '+' : 10,
    '-' : -10,
    '0' : -1
}
