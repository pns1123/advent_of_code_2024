with open("puzzle.input", "r") as fp:
    lines = [l.rstrip() for l in fp.readlines()]


def check_horizontal(i, j, lines):
    return lines[i][j : j + 4] == "XMAS"


def check_vertical(i, j, lines):
    return "".join([l[j] for l in lines[i : i + 4]]) == "XMAS"


def check_diagonal_top(i, j, lines):
    return (
        "".join([l[j + k] for k, l in enumerate(lines[i - 3 : i + 1][::-1])]) == "XMAS"
    )


def check_diagonal_bottom(i, j, lines):
    return "".join([l[j + k] for k, l in enumerate(lines[i : i + 4])]) == "XMAS"


def check_horizontal_reversed(i, j, lines):
    return lines[i][j - 3 : j + 1][::-1] == "XMAS"


def check_vertical_reversed(i, j, lines):
    return "".join([l[j] for l in lines[i - 3 : i + 1][::-1]]) == "XMAS"


def check_diagonal_top_reversed(i, j, lines):
    return (
        "".join([l[j - k] for k, l in enumerate(lines[i - 3 : i + 1][::-1])])
        == "XMAS"[::1]
    )


def check_diagonal_bottom_reversed(i, j, lines):
    return "".join([l[j - k] for k, l in enumerate(lines[i : i + 4])]) == "XMAS"[::1]


def count_xmas_occurences(i, j, lines):
    n_rows, n_cols = len(lines), len(lines[0])
    count = 0
    if j + 3 < n_cols:
        count += check_horizontal(i, j, lines)
    if i + 3 < n_rows:
        count += check_vertical(i, j, lines)
    if i - 3 >= 0 and j + 3 < n_cols:
        count += check_diagonal_top(i, j, lines)
    if i + 3 < n_rows and j + 3 < n_cols:
        count += check_diagonal_bottom(i, j, lines)

    if j - 3 >= 0:
        count += check_horizontal_reversed(i, j, lines)
    if i - 3 >= 0:
        count += check_vertical_reversed(i, j, lines)
    if i - 3 >= 0 and j - 3 >= 0:
        count += check_diagonal_top_reversed(i, j, lines)
    if i + 3 < n_rows and j - 3 >= 0:
        count += check_diagonal_bottom_reversed(i, j, lines)
    return count


def count_x_mas_occurences(i, j, lines):
    n_rows, n_cols = len(lines), len(lines[0])

    if i == 0 or i == n_rows - 1 or j == 0 or j == n_cols - 1:
        # center cannot be on the boundary
        return False

    return "".join([lines[i - 1][j - 1], lines[i][j], lines[i + 1][j + 1]]) in [
        "MAS",
        "SAM",
    ] and "".join([lines[i - 1][j + 1], lines[i][j], lines[i + 1][j - 1]]) in [
        "MAS",
        "SAM",
    ]


n_rows, n_cols = len(lines), len(lines[0])
xmas_position_counts = [
    ((i, j), count_xmas_occurences(i, j, lines))
    for i in range(n_cols)
    for j in range(n_rows)
]

x_mas_position_counts = [
    ((i, j), count_x_mas_occurences(i, j, lines))
    for i in range(n_cols)
    for j in range(n_rows)
]

print("q1", sum([occ for _, occ in xmas_position_counts]))
print("q2", sum([occ for _, occ in x_mas_position_counts]))
