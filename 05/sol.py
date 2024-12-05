with open("puzzle.input", "r") as fp:
    lines = [l.strip() for l in fp.readlines()]

ordering_rules = [tuple(s.split("|")) for s in lines[: lines.index("")]]
updates = [s.split(",") for s in lines[lines.index("") + 1 :]]


def check_update(update):
    for i, pn in enumerate(update):
        if lookup.get(pn, set()) & set(update[i + 1 :]):
            return False
    return True


def repair_update(update):
    adjacency_dict = {
        k: filtered_neighbors.copy()
        for k in update
        if len(
            (
                filtered_neighbors := set(
                    filter(lambda x: x in update, lookup.get(k, set()))
                )
            )
        )
    }

    order = topological_sort(set(update), adjacency_dict)

    return sorted(update, key=lambda k: order.index(k))


def topological_sort(alphabet, adjacency_dict):
    L = []
    S = alphabet.difference(set(adjacency_dict.keys()))

    while len(S) > 0:
        n = S.pop()
        L.append(n)
        for m in [k for k, v in adjacency_dict.items() if n in v]:
            adjacency_dict[m].remove(n)
            if len(adjacency_dict[m]) == 0:
                S.add(m)
    for _, v in adjacency_dict.items():
        if len(v) > 0:
            raise ValueError("graph has at least one cycle")

    return L

lookup = {}
for a, b in ordering_rules:
    cur = lookup.get(b, set())
    cur.add(a)
    lookup[b] = cur


print("q1", sum([int(u[len(u) // 2]) for u in updates if check_update(u)]))
print(
    "q2",
    sum([int(repair_update(u)[len(u) // 2]) for u in updates if not check_update(u)]),
)
