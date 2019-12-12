from functools import reduce
from itertools import combinations, groupby
from operator import mul


def third_groups(sizes, groups=3, target=None):
    if groups == 1:
        yield (tuple(sizes),)
        return
    if target is None:
        target = sum(sizes) // groups
    for l in range(1, len(sizes)):
        for combo in combinations(sizes, l):
            if sum(combo) != target:
                continue
            remaining = set(sizes).difference(combo)
            for res in third_groups(remaining, groups - 1, target):
                yield (combo,) + res


def min_quantum_entanglement(sizes, groups=3):
    # the way I build the groups puts the smallest quantum entanglement first
    return reduce(mul, next(third_groups(sizes, groups))[0])


if __name__ == '__main__':
    import sys
    filename = sys.argv[-1]
    with open(filename) as f:
        sizes = [int(l) for l in f]

    print('Part 1:', min_quantum_entanglement(sizes))
    print('Part 2:', min_quantum_entanglement(sizes, 4))
