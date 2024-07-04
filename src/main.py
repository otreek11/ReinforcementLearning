from globals import *
from sys import exit
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import choice, randint

Q = {}
get_Qstate = lambda state: Q.get(state, { direction: 0 for direction in DIRECTIONS })
get_Qval = lambda state, action: get_Qstate(state).get(action, 0)
vector_add = lambda v1, v2: (v1[0] + v2[0], v1[1] + v2[1])

def choose_action(state):
    valid = valid_actions(state[0])
    if EPSILON.roll():
        return choice(valid)
    
    Qstate = get_Qstate(state)
    max_val = Qstate.get(valid[0], 0)
    max_action = valid[0]

    for direction in valid:
        if Qstate.get(direction, 0) > max_val:
            max_val = get_Qval(state, direction)
            max_action = direction

    return max_action

def valid_actions(robot_pos):
    valid = []
    for direction in DIRECTIONS:
        new_pos = vector_add(robot_pos, direction)
        if MAP_CONTAINS(new_pos):
            valid.append(direction)
    
    return valid

def initialize_map():
    robot_pos = None
    objec_pos = None
    obsta_pos = None

    for row_idx, row in enumerate(MAP):
        for col_idx, col in enumerate(row):
            if col == 'K':
                obsta_pos = (col_idx, row_idx)
            elif col == 'R':
                robot_pos = (col_idx, row_idx)
            elif col == 'X':
                objec_pos = (col_idx, row_idx)

    if robot_pos is None or objec_pos is None or obsta_pos is None:
        print("Error! Could not initialize all necessary objects!")
        exit(0)

    return (robot_pos, objec_pos, obsta_pos)

def training(epochs) -> int:
    global robot, obj, obst, Q
    irobot, iobst = robot, obst

    collisions = 0
    for i in range(epochs):
        robot, obst = irobot, iobst
        state = (robot, obst)
        action = choose_action(state)
        while robot != obj and robot != obst:
            new_robot = vector_add(robot, action)
            if MAP_CONTAINS(new_robot):
                robot = new_robot
            else:
                Q[state][action] = -float('inf')
            obst = vector_add(obst, (0, randint(1, 3)))
            obst = (obst[0], obst[1] % MAP_HEIGHT)
            new_state = (robot, obst)

            reinforcement = REWARDS['0']
            if robot == obst: reinforcement = REWARDS['-']
            elif robot == obj: reinforcement = REWARDS['+']

            new_action = choose_action(new_state)

            if state not in Q:
                Q[state] = { direction : 0 for direction in DIRECTIONS }

            currqval = get_Qval(state, action)
            nextqval = get_Qval(new_state, new_action)
            Q[state][action] = currqval + CONSTANTS['alpha'] * (reinforcement + CONSTANTS['gamma'] * nextqval - currqval)

            if reinforcement != REWARDS['0']:
                if reinforcement == REWARDS['-']:
                    collisions += 1
                break

            state = new_state
            action = new_action

    robot, obst = irobot, iobst
    for state in Q.keys():
        for direction in Q[state]:
            pos = vector_add(state[0], direction)
            if not MAP_CONTAINS(pos):
                Q[state][direction] = -float('inf')

    return collisions

if __name__ == '__main__':
    robot, obj, obst = initialize_map()
    epochs = int(input("Insert number of epochs: "))
    print("Training...")
    coll = training(epochs)

    print(f"{'-'*20} TRAINING COMPLETE! {'-'*20}")
    print(f"Number of Collisions: {coll} ({coll*100/epochs:.2f}%)")

    path = []
    obst_path = []
    state = (robot, obst)
    print(f"{'-'*20} GREEDY TRAJECTORY: {'-'*20}")
    while robot != obj and robot != obst:
        action = choose_action(state)
        new_robot = vector_add(robot, action)
        if MAP_CONTAINS(new_robot):
            robot = new_robot
        obst = vector_add(obst, (0, randint(1, 3)))
        obst = (obst[0], obst[1] % MAP_HEIGHT)
        path.append(robot)
        obst_path.append(obst)
        print(f"Robot: {robot}, Obstacle: {obst}")
        if robot == obst:
            print(f"{'-'*20} COLLISION DETECTED! {'-'*20}")
            break
        elif robot == obj:
            print(f"{'-'*20} GOAL REACHED! {'-'*20}")
            break

        state = (robot, obst)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(0, MAP_WIDTH)
    ax.set_ylim(MAP_HEIGHT, 0)
    ax.set_title('Greedy Trajectory Animation')

    ax.scatter(obj[0], obj[1], color='green', marker='*', s=200)

    robot_plot, = ax.plot([], [], 'bo', markersize=10)
    obst_plot, = ax.plot([], [], 'rs', markersize=10)
    path_line, = ax.plot([], [], 'g-', lw=1)
    obst_path_line, = ax.plot([], [], 'k-', lw=1)

    def init():
        return []

    def animate(i):
        if i < len(path):
            robot_plot.set_data([path[i][0]], [path[i][1]])
            obst_plot.set_data([obst_path[i][0]], [obst_path[i][1]])
            path_line.set_data([step[0] for step in path[:i+1]], [step[1] for step in path[:i+1]])
            obst_path_line.set_data([step[0] for step in obst_path[:i+1]], [step[1] for step in obst_path[:i+1]])

        return [robot_plot, obst_plot, path_line, obst_path_line]

    ani = animation.FuncAnimation(fig, animate, frames=len(path), init_func=init, blit=True)
    plt.show()