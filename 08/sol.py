with open("puzzle.input", "r") as fp:
    lines = [l.strip() for l in fp.readlines()]


def is_on_grid(loc, lines):
    row, col = loc
    n_rows, n_cols = len(lines), len(lines[0])
    return 0 <= row < n_rows and 0 <= col < n_cols


def construct_antinodes_v1(
    pair: tuple[tuple[int, int], tuple[int, int]]
) -> list[tuple[int, int]]:
    ((r1, c1), (r2, c2)) = pair
    row_diff, col_diff = r2 - r1, c2 - c1
    return [(r1 - row_diff, c1 - col_diff), (r2 + row_diff, c2 + col_diff)]


def construct_antinodes_v2(
    pair: tuple[tuple[int, int], tuple[int, int]]
) -> list[tuple[int, int]]:
    ((r1, c1), (r2, c2)) = pair
    row_diff, col_diff = r2 - r1, c2 - c1
    an1 = [(r1, c1)]
    while True:
        r, c = an1[-1]
        candidate_an = (r - row_diff, c - col_diff)
        if not is_on_grid(candidate_an, lines):
            break
        an1.append(candidate_an)
    an2 = [(r2, c2)]
    while True:
        r, c = an2[-1]
        candidate_an = (r + row_diff, c + col_diff)
        if not is_on_grid(candidate_an, lines):
            break
        an2.append(candidate_an)

    return an1 + an2


antennas = {}
for row in range(len(lines)):
    for col in range(len(lines[0])):
        if lines[row][col] != ".":
            antennas[lines[row][col]] = [*antennas.get(lines[row][col], []), (row, col)]

pairs = {
    freq: [(l1, l2) for i1, l1 in enumerate(locations) for l2 in locations[i1 + 1 :]]
    for freq, locations in antennas.items()
}

anti_nodes_v1 = {
    freq: [
        p
        for positions in [construct_antinodes_v1(pair) for pair in pairs]
        for p in positions
    ]
    for freq, pairs in pairs.items()
}

anti_nodes_v2 = {
    freq: [
        p
        for positions in [construct_antinodes_v2(pair) for pair in pairs]
        for p in positions
    ]
    for freq, pairs in pairs.items()
}


print(
    "q1",
    len(
        set(
            [
                an
                for positions in anti_nodes_v1.values()
                for an in positions
                if is_on_grid(an, lines)
            ]
        )
    ),
)

print(
    "q2",
    len(
        set(
            [
                an
                for positions in anti_nodes_v2.values()
                for an in positions
                if is_on_grid(an, lines)
            ]
        )
    ),
)
