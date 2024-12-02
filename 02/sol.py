from functools import reduce

with open("puzzle.input", "r") as fp:
    lines = fp.readlines()

reports = [[int(n) for n in l.split()] for l in lines]


def is_valid_increment(xy):
    return 1 <= xy[1] - xy[0] <= 3


def is_valid_decrement(xy):
    return 1 <= xy[0] - xy[1] <= 3


def is_valid_increasing(l):
    return reduce(
        lambda acc, xy: acc and is_valid_increment(xy),
        zip(l, l[1:]),
        True,
    )


def is_valid_decreasing(l):
    return reduce(
        lambda acc, xy: acc and is_valid_decrement(xy),
        zip(l, l[1:]),
        True,
    )


def is_safe_report_q1(l):
    return is_valid_increasing(l) or is_valid_decreasing(l)


def is_valid_increasing_dampened(r, k):
    if k == len(r) - 2:
        return True
    if is_valid_increment((r[k], r[k + 1])):
        return is_valid_increasing_dampened(r, k + 1)
    else:
        return is_valid_increasing(r[:k] + r[k + 1 :]) or is_valid_increasing(
            r[: k + 1] + r[k + 2 :]
        )


def is_valid_decreasing_dampened(r, k):
    if k == len(r) - 2:
        return True
    if is_valid_decrement((r[k], r[k + 1])):
        return is_valid_decreasing_dampened(r, k + 1)
    else:
        return is_valid_decreasing(r[:k] + r[k + 1 :]) or is_valid_decreasing(
            r[: k + 1] + r[k + 2 :]
        )


def is_safe_report_q2(r):
    return is_valid_increasing_dampened(r, 0) or is_valid_decreasing_dampened(r, 0)


print("q1:", sum([is_safe_report_q1(r) for r in reports]))
print("q2:", sum([is_safe_report_q2(r) for r in reports]))
