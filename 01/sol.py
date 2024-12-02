with open("puzzle.input", "r") as fp:
    lines = fp.readlines()

pairs = [[int(s) for s in l.split()] for l in lines]
listA = [p[0] for p in pairs]
listB = [p[1] for p in pairs]

distances = [abs(a - b) for a, b in zip(sorted(listA), sorted(listB))]
print("q1:", sum(distances))

counts = {}
for j in listB:
    counts[j] = counts.get(j, 0) + 1

print("q2:", sum([counts.get(k, 0) * k for k in listA]))
