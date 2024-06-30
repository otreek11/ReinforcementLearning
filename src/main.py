import numpy as np
from globals import *
from robot import *
from obstacle import *
from point import *

# TODO: Correct erros and understand code

def training(epochs: int) -> np.ndarray:
    global robot, obstacle, objective
    Q = np.zeros((MAP_HEIGHT, MAP_WIDTH, MAP_HEIGHT, MAP_WIDTH, 8))
    for _ in range(epochs):
        robot.reset()
        obstacle.reset()
        action = robot.choose_action(obstacle, Q)

        while (not robot.collides_with(objective)) and (not robot.collides_with(obstacle)):
            next_robot = robot.next(action)
            next_obstacle = obstacle.next()

            reward = VALUES['none']
            if robot.collides_with(objective):
                reward = VALUES['reward']
            elif robot.collides_with(obstacle):
                reward = VALUES['punishment']

            next_action = next_robot.choose_action(next_obstacle, Q)
            Q[robot.col, robot.row, obstacle.col, obstacle.row, action] += CONSTANTS['alpha'] * (reward + CONSTANTS['gamma'] * Q[next_robot.col, next_robot.row, next_obstacle.col, next_obstacle.row] - Q[robot.col, robot.row, obstacle.col, obstacle.row])
            if reward == VALUES['reward'] or reward == VALUES['punishment']:
                break

            action = next_action
            robot.do_next(next_robot)
            obstacle.do_next(next_obstacle)

    robot.reset()
    obstacle.reset()
    return Q


def initialize_map(map: list[str]) -> tuple[Robot, Obstacle, Point]:
    robot = None
    obstacle = None
    objective = None
    for row in map:
        for col in row:
            if col == 'R':
                robot = Robot(col, row)
            elif col == 'K':
                obstacle = Obstacle(col, row)
            elif col == 'E':
                objective = Point(col, row)

    return (robot, obstacle, objective)

if __name__ == "__main__":
    robot, obstacle, objective = initialize_map(MAP)
    epochs = None
    while (epochs == None):
        epochs = input("Insert number of epochs: ")
        try:
            epochs = int(epochs)
        except:
            print("Invalid entry!")
            epochs = None
    
    Q = training(epochs)
    path = [Point(robot)]

    while not robot.collides_with(objective):
        action = np.argmax(Q[robot.col, robot.row, obstacle.col, obstacle.row])
        robot.do_next(robot.next(action))
        obstacle.do_next(obstacle.next())
        path.append(Point(robot))
        print(f"Robot: {robot}, Obstacle: {obstacle}")
        if robot.collides_with(obstacle):
            print("Collision detected!")
            break

    print(f"Path: {path}")