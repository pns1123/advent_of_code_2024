with open("puzzle.input", "r") as fp:
    lines = [l.strip() for l in fp.readlines()]


def prepare_line(l: str) -> (int, list[int]):
    [res, nums] = l.split(":")
    return (int(res), [int(n) for n in nums.split()])


def check_binary_line(pl: (int, list[int])) -> bool:
    (res, nums) = pl

    def right(i: int) -> int:
        return 2 * i + 2

    def left(i: int) -> int:
        return 2 * i + 1

    bfs = [None for _ in range(2 ** len(nums) - 1)]
    bfs[0] = nums[0]
    for i in range(2 ** (len(nums) - 1) - 1):
        # print(i, bfs[i], right(i), left(i), (i + 1).bit_length(), bfs)
        bfs[right(i)] = bfs[i] + nums[(i + 1).bit_length()]
        bfs[left(i)] = bfs[i] * nums[(i + 1).bit_length()]

    return res in bfs


def check_ternary_line_recursive(nums, res, acc) -> bool:
    if len(nums) == 0:
        return acc == res
    n = nums[0]
    return (
        check_ternary_line_recursive(nums[1:], res, int(str(acc) + str(n)))
        or check_ternary_line_recursive(nums[1:], res, acc + n)
        or check_ternary_line_recursive(nums[1:], res, acc * n)
    )


prepared_lines = [prepare_line(l) for l in lines]
print(
    "q1", sum([res for (res, nums) in prepared_lines if check_binary_line((res, nums))])
)
print(
    "q2",
    sum(
        [
            res
            for (res, nums) in prepared_lines
            if check_ternary_line_recursive(nums[1:], res, nums[0])
        ]
    ),
)
