import random
from queue import Queue, LifoQueue, PriorityQueue

# Helper functions
def is_solvable(grid):
    flattened = [cell for row in grid for cell in row if cell != 0]
    inv_count = 0
    for i in range(len(flattened) - 1):
        for j in range(i + 1, len(flattened)):
            if flattened[i] > flattened[j]:
                inv_count += 1
    return inv_count % 2 == 0

def generate_random_grid():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # 'B' is represented by 0
    random.shuffle(numbers)
    grid = [numbers[i:i+3] for i in range(0, len(numbers), 3)]
    while not is_solvable(grid):
        random.shuffle(numbers)
        grid = [numbers[i:i+3] for i in range(0, len(numbers), 3)]
    return grid

def get_position(state, element=0):  # 'B' is represented by 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == element:
                return (i, j)

def get_children(node):
    x, y = get_position(node)
    children = []
    for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x, new_y = x + move[0], y + move[1]
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = [row.copy() for row in node]
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            children.append(new_state)
    return children

# Search algorithms
def bfs(start, goal):
    queue = Queue()
    queue.put((start, 0))
    seen = set()
    while not queue.empty():
        state, depth = queue.get()
        if tuple(map(tuple, state)) in seen:
            continue
        if state == goal:
            return depth
        seen.add(tuple(map(tuple, state)))
        for child in get_children(state):
            if tuple(map(tuple, child)) not in seen:
                queue.put((child, depth + 1))
    return None

def dfs(start, goal, depth_limit=15):
    stack = LifoQueue()
    stack.put((start, 0))
    seen = set()
    while not stack.empty():
        state, depth = stack.get()
        if tuple(map(tuple, state)) in seen or depth > depth_limit:
            continue
        if state == goal:
            return depth
        seen.add(tuple(map(tuple, state)))
        for child in get_children(state):
            if tuple(map(tuple, child)) not in seen:
                stack.put((child, depth + 1))
    return None

def ucs(start, goal):
    pqueue = PriorityQueue()
    pqueue.put((0, start))
    seen = set()
    while not pqueue.empty():
        cost, state = pqueue.get()
        if tuple(map(tuple, state)) in seen:
            continue
        if state == goal:
            return cost
        seen.add(tuple(map(tuple, state)))
        for child in get_children(state):
            if tuple(map(tuple, child)) not in seen:
                pqueue.put((cost + 1, child))
    return None

def ids(start, goal, max_depth=15):
    for depth in range(max_depth):
        result = dfs(start, goal, depth)
        if result is not None:
            return result
    return None

# Main execution
start_state = generate_random_grid()
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # 'B' is represented by 0

bfs_steps = bfs(start_state, goal_state)
dfs_steps = dfs(start_state, goal_state)
ucs_steps = ucs(start_state, goal_state)
ids_steps = ids(start_state, goal_state, 30)  # I've increased the max depth a bit for IDS

print(f"BFS took {bfs_steps} steps.")
print(f"DFS took {dfs_steps} steps.")
print(f"UCS took {ucs_steps} steps.")
print(f"IDS took {ids_steps} steps.")
