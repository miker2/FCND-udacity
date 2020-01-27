from enum import Enum
from queue import PriorityQueue
import numpy as np

class Action(Enum):
    """
    An action is represented by a 3 element tuple.

    The first 2 values are the delta of the action relative
    to the current grid position. The third and final value
    is the cost of performing the action.
    """
    UP = (-1, 0, 1)
    URIGHT = (-1, 1, np.math.sqrt(2))
    RIGHT = (0, 1, 1)
    DRIGHT = (1, 1, np.math.sqrt(2))
    DOWN = (1, 0, 1)
    DLEFT = (1, -1, np.math.sqrt(2))
    LEFT = (0, -1, 1)
    ULEFT = (-1, -1, np.math.sqrt(2))
    
    def __str__(self):
        if self == self.UP:
            return '↑'
        elif self == self.URIGHT:
            return '↗'
        elif self == self.RIGHT:
            return '→'
        elif self == self.DRIGHT:
            return '↘'
        elif self == self.DOWN:
            return '↓'
        elif self == self.DLEFT:
            return '↙'
        elif self == self.LEFT:
            return '←'
        elif self == self.ULEFT:
            return '↖'

    @property
    def cost(self):
        return self.value[2]

    @property
    def delta(self):
        return (self.value[0], self.value[1])


def valid_actions(grid, current_node):
    """
    Returns a list of valid actions given a grid and current node.
    """
    #valid = [Action.UP, Action.LEFT, Action.RIGHT, Action.DOWN]
    valid = [a for a in Action]
    n, m = grid.shape[0] - 1, grid.shape[1] - 1
    x, y = current_node

    # check if the node is off the grid or
    # it's an obstacle

    for a in Action:
        new_x = x + a.delta[0]
        new_y = y + a.delta[1]
        # Check if the node is off the grid
        if new_x < 0 or new_x > n or new_y < 0 or new_y > m:
            valid.remove(a)
        # Check if the node is an obstacle
        elif grid[new_x, new_y] == 1:
            valid.remove(a)

    return valid


def a_star(grid, h, start, goal):

    queue = PriorityQueue()
    queue.put((0, start))
    visited = set(start)

    branch = {}
    found = False
    
    while not queue.empty():
        item = queue.get()
        current_node = item[1]
        if current_node == start:
            current_cost = 0.0
        else:              
            current_cost = branch[current_node][0]
            
        if current_node == goal:        
            print('Found a path.')
            found = True
            break
        else:
            for action in valid_actions(grid, current_node):
                # get the tuple representation
                da = action.delta
                next_node = (current_node[0] + da[0], 
                             current_node[1] + da[1])
                branch_cost = current_cost + action.cost
                queue_cost = branch_cost + h(next_node, goal)
                
                if next_node not in visited:                
                    visited.add(next_node)               
                    branch[next_node] = (branch_cost, current_node, action)
                    queue.put((queue_cost, next_node))
             
    path = []
    path_cost = 0
    if found:
        # retrace steps
        n = goal
        path_cost = branch[n][0]
        path.append(goal)
        while branch[n][1] != start:
            path.append(branch[n][1])
            n = branch[n][1]
        path.append(branch[n][1])
    else:
        print('**********************')
        print('Failed to find a path!')
        print('**********************') 
    return path[::-1], path_cost

