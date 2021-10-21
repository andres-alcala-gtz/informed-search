from pyamaze import pyamaze, maze, agent, textLabel
from queue import PriorityQueue


# manhattan distance
def h(current:tuple, goal:tuple) -> int:
    current_x, current_y = current
    goal_x, goal_y = goal
    return abs(current_x - goal_x) + abs(current_y - goal_y)


# searching algorithm
def greedy(maze:pyamaze.maze) -> tuple:

    # important cells
    start = (maze.rows, maze.cols)
    goal = maze._goal

    # open list
    open = PriorityQueue()
    open.put((h(start, goal), h(start, goal), start))

    # costs
    f_cost = {row:float('inf') for row in maze.grid}
    f_cost[start] = h(start, goal)

    # paths
    backward = {}
    forward = {}
    search = [start]

    while not open.empty():

        current = open.get()[2]
        search.append(current)

        if current == goal:
            break

        for direction in ['N', 'S', 'W', 'E']:

            if maze.maze_map[current][direction]:

                if direction == 'N':
                    successor = (current[0]-1, current[1])
                elif direction == 'S':
                    successor = (current[0]+1, current[1])
                elif direction == 'W':
                    successor = (current[0], current[1]-1)
                elif direction == 'E':
                    successor = (current[0], current[1]+1)

                f_temp = h(successor, goal)

                if f_temp < f_cost[successor]:
                    backward[successor] = current
                    f_cost[successor] = f_temp
                    open.put((f_cost[successor], h(successor, goal), successor))

    cell = goal
    while cell != start:
        forward[backward[cell]] = cell
        cell = backward[cell]

    return search, forward


# main
if __name__ == '__main__':

    maze = maze()
    maze.CreateMaze(loadMaze='input.csv', theme='light')

    search, path = greedy(maze)

    agent_search = agent(parentMaze=maze, footprints=True, color='blue', filled=True)
    agent_path = agent(parentMaze=maze, footprints=True, color='yellow')

    maze.tracePath({agent_search:search})
    maze.tracePath({agent_path:path})

    label = textLabel(parentMaze=maze, title='Searching Algorithm', value='Greedy')
    label = textLabel(parentMaze=maze, title='Search Length', value=len(search))
    label = textLabel(parentMaze=maze, title='Path Length', value=len(path)+1)

    maze.run()