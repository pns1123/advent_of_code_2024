from collections import deque

with open("puzzle.input", "r") as fp:
    lines = [l.strip() for l in fp.readlines()]

grid = [[int(k) for k in l] for l in lines]

trail_heads = []
for row in range(len(grid)):
    for col in range(len(grid[0])):
        if grid[row][col] == 0:
            trail_heads.append((row, col))


def count_trails(grid, root):
    trail_counter = 0
    explored = {root}
    queue = deque([root])
    while len(queue) > 0:
        v_row, v_col = queue.popleft()
        if grid[v_row][v_col] == 9:
            trail_counter += 1
        for w in neigh((v_row, v_col), grid):
            if w not in explored:
                explored.add(w)
                queue.append(w)
    return trail_counter


def compute_rating(grid, root):
    trail_counter = 0
    queue = deque([[root]])
    while len(queue) > 0:
        path = queue.popleft()
        v_row, v_col = path[-1]
        if grid[v_row][v_col] == 9:
            trail_counter += 1
        for w in neigh((v_row, v_col), grid):
            if w not in path:
                path = [*path.copy(), w]
                queue.append(path)
    return trail_counter


def neigh(v, grid):
    v_row, v_col = v
    return [
        w
        for w in [
            (v_row - 1, v_col),
            (v_row, v_col + 1),
            (v_row + 1, v_col),
            (v_row, v_col - 1),
        ]
        if is_on_grid(w, grid) and is_valid_increment(v, w, grid)
    ]


def is_on_grid(v, grid):
    v_row, v_col = v
    return 0 <= v_row < len(grid) and 0 <= v_col < len(grid[0])


def is_valid_increment(v, w, grid):
    v_row, v_col = v
    w_row, w_col = w
    return grid[w_row][w_col] - grid[v_row][v_col] == 1


print("q1", sum([count_trails(grid, th) for th in trail_heads]))

print("q2", sum([compute_rating(grid, th) for th in trail_heads]))
