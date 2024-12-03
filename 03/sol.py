import re

with open("puzzle.input", "r") as fp:
    lines = fp.readlines()


def extract_valid_mul(l):
    pattern = r"mul\(\d{1,3},\d{1,3}\)"
    return re.findall(pattern, l)


def extract_factors(mul):
    pattern = r"\d{1,3}"
    return re.findall(pattern, mul)


def multiply(factors):
    [a, b] = factors
    return int(a) * int(b)


def linesum(line):
    return sum([multiply(extract_factors(m)) for m in extract_valid_mul(line)])


def split_line(l, do_sections=[], do_mode=True):
    pattern = r"(do\(\))|(don't\(\))"
    match_result = re.search(pattern, l)

    if match_result is None:
        return [*do_sections, l] if do_mode else do_sections
    else:
        if do_mode:
            do_sections = [*do_sections, l[: match_result.start()]]
        match match_result.group():
            case "do()":
                return split_line(l[match_result.end() :], do_sections, do_mode=True)
            case "don't()":
                return split_line(l[match_result.end() :], do_sections, do_mode=False)
            case _:
                raise ValueError(f"{match_result.group()} unknown")


print("q1:", linesum("".join(lines)))
print("q2:", sum([linesum(do_section) for do_section in split_line("".join(lines))]))
