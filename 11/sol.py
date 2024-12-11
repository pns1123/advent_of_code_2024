with open("puzzle.input", "r") as fp:
    initial_stones = [int(k) for k in fp.readlines()[0].split()]


def split_stone(n: int) -> [int]:
    if n == 0:
        return [1]
    if len(str(n)) % 2 == 0:
        half = len(str(n)) // 2
        return [int(str(n)[:half]), int(str(n)[half:])]
    return [2024 * n]


def blink(stones):
    return [j for k in [split_stone(s) for s in stones] for j in k]


def blink_k_times(k, f, stones):
    for j in range(k):
        stones = f(stones)
    return stones


def blink_w_dict(stone_counts: dict) -> dict:
    new_stone_counts = {}
    for k, count in stone_counts.items():
        new_stone_counts = add_count(new_stone_counts, split_stone(k), incr=count)
    return new_stone_counts


def add_count(count: dict, xs: list, incr=1):
    for s in xs:
        count[s] = count.get(s, 0) + incr
    return count


print("q1", len(blink_k_times(25, blink, initial_stones)))
print(
    "q2", sum(blink_k_times(75, blink_w_dict, add_count({}, initial_stones)).values())
)
