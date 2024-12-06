import sys

sys.setrecursionlimit(10000)

with open("puzzle.input", "r") as fp:
    lines = [l.strip() for l in fp.readlines()]


for i, l in enumerate(lines):
    if len(set(l).difference({"#", "."})) > 0:
        initial_position = (l.index("^"), i)


DIRECTION = [
    (0, -1),  # UP
    (1, 0),  # RIGHT
    (0, 1),  # DOWN
    (-1, 0),  # LEFT
]


def is_on_grid(position, grid):
    x, y = position
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def trace_path(position, direction_index, grid, trace):
    if not is_on_grid(position, grid):
        return trace
    else:
        x, y = position
        if grid[y][x] == "#":
            new_direction_index = (direction_index + 1) % 4
            # print(
            #     "obstacle detected at",
            #     (x, y),
            #     "changing direction to",
            #     DIRECTION[new_direction_index],
            #     trace,
            # )
            dx_old, dy_old = DIRECTION[direction_index]
            dx_new, dy_new = DIRECTION[new_direction_index]
            return trace_path(
                (x - dx_old + dx_new, y - dy_old + dy_new),
                new_direction_index,
                grid,
                trace,
            )
        else:
            dx, dy = DIRECTION[direction_index]
            return trace_path((x + dx, y + dy), direction_index, grid, [*trace, (x, y)])


def trace_path_iter(position, direction_index, grid, trace):
    while is_on_grid(position, grid):
        x, y = position
        if grid[y][x] == "#":
            dx_old, dy_old = DIRECTION[direction_index]
            direction_index = (direction_index + 1) % 4
            dx_new, dy_new = DIRECTION[direction_index]
            position = (x - dx_old + dx_new, y - dy_old + dy_new)
        else:
            dx, dy = DIRECTION[direction_index]
            position = (x + dx, y + dy)
            trace = [*trace, (x, y)]

    return trace


def check_if_cycle_brute_force(position, direction_index, grid, directed_trace):
    while True:
        if not is_on_grid(position, grid):
            return False
        if (position, direction_index) in directed_trace:
            return True

        x, y = position
        if grid[y][x] == "#":
            dx_old, dy_old = DIRECTION[direction_index]
            direction_index = (direction_index + 1) % 4
            dx_new, dy_new = DIRECTION[direction_index]
            position = (x - dx_old + dx_new, y - dy_old + dy_new)
        else:
            dx, dy = DIRECTION[direction_index]
            position = (x + dx, y + dy)
            directed_trace = [*directed_trace, ((x, y), direction_index)]


def count_loop_barrier_position(initial_position, trace, grid):
    counter = 0
    for i, (x_obstacle, y_obstacle) in enumerate(trace.difference({initial_position})):
        print(i, "/", len(trace) - 1)
        lines[y_obstacle] = (
            lines[y_obstacle][:x_obstacle] + "#" + lines[y_obstacle][x_obstacle + 1 :]
        )
        # if check_if_cycle_brute_force(initial_position, 0, lines, []):
        if check_if_cycle_floyd(initial_position, 0, lines):
            counter += 1
        lines[y_obstacle] = (
            lines[y_obstacle][:x_obstacle] + "." + lines[y_obstacle][x_obstacle + 1 :]
        )

    return counter


def take_step(position, direction_index, grid):
    if not is_on_grid(position, grid):
        raise ValueError

    x, y = position
    if grid[y][x] == "#":
        dx_old, dy_old = DIRECTION[direction_index]
        direction_index = (direction_index + 1) % 4
        dx_new, dy_new = DIRECTION[direction_index]
        return (x - dx_old + dx_new, y - dy_old + dy_new), direction_index, grid
    else:
        dx, dy = DIRECTION[direction_index]
        return (x + dx, y + dy), direction_index, grid


def check_if_cycle_floyd(position, direction_index, grid):
    tortoise = take_step(position, direction_index, grid)
    hare = take_step(*take_step(position, direction_index, grid))
    while tortoise != hare:
        try:
            tortoise = take_step(*tortoise)
            hare = take_step(*take_step(*hare))
        except ValueError:
            return False
    return True


trace = set(trace_path_iter(initial_position, 0, lines, []))
print("q1", len(trace))
print("q2", count_loop_barrier_position(initial_position, trace, lines))
