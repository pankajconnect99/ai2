import random
from queue import PriorityQueue

# Helper Functions
def is_solvable(grid):
    flattened = [cell for row in grid for cell in row if cell != 'B']
    inv_count = 0
    for i in range(len(flattened) - 1):
        for j in range(i + 1, len(flattened)):
            if flattened[i] > flattened[j]:
                inv_count += 1
    return inv_count % 2 == 0

def generate_random_grid():
    while True:
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 'B']
        random.shuffle(numbers)
        grid = [numbers[i:i + 3] for i in range(0, len(numbers), 3)]
        if is_solvable(grid):
            return grid

def get_position(state, element='B'):
    for i in range(3):
        for j in range(3):
            if state[i][j] == element:
                return (i, j)

# Node Class
class PuzzleNode:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth

    def get_children(self):
        x, y = get_position(self.state)
        children = []
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Right, Left, Down, Up
            new_x, new_y = x + move[0], y + move[1]
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = [row.copy() for row in self.state]
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                children.append(PuzzleNode(new_state, self, move, self.depth + 1))
        return children

# UCS Algorithm
def ucs(start, goal):
    start_node = PuzzleNode(start)
    frontier = PriorityQueue()
    counter = 0
    frontier.put((0, counter, start_node))
    explored = set()

    while not frontier.empty():
        _, _, current = frontier.get()

        if tuple(map(tuple, current.state)) == tuple(map(tuple, goal)):
            return current

        explored.add(tuple(map(tuple, current.state)))
        for child in current.get_children():
            if tuple(map(tuple, child.state)) not in explored:
                counter += 1
                frontier.put((child.depth, counter, child))

    return None

# IDS Algorithm
def ids(start, goal, max_depth):
    for depth in range(max_depth):
        found = dls(PuzzleNode(start), goal, depth)
        if found:
            return found
    return None

def dls(node, goal, limit):
    if node.state == goal:
        return node
    elif limit <= 0:
        return None
    else:
        for child in node.get_children():
            result = dls(child, goal, limit - 1)
            if result:
                return result
    return None

# Main
start_state = generate_random_grid()
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 'B']]

print(f"Start state:")
for row in start_state:
    print(row)

solution_ucs = ucs(start_state, goal_state)
if solution_ucs:
    print("\nSolution found using UCS!")
else:
    print("\nNo solution found using UCS.")

solution_ids = ids(start_state, goal_state, 25)
if solution_ids:
    print("Solution found using IDS!")
else:
    print("No solution found using IDS.")
