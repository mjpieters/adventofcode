from itertools import combinations


def combos_for_size(containers, size):
    return sum(
        1
        for count in range(len(containers))
        for c in combinations(containers, count + 1)
        if sum(c) == size)


def combos_for_min_size(containers, size):
    min_count = next(
        count
        for count in range(len(containers))
        for c in combinations(containers, count + 1)
        if sum(c) == size)
    return sum(
        1
        for c in combinations(containers, min_count + 1)
        if sum(c) == size)


if __name__ == '__main__':
    import sys

    filename = sys.argv[-1]
    with open(filename) as inputfile:
        containers = [int(l) for l in inputfile if l.strip()]

    print('Part 1:', combos_for_size(containers, 150))
    print('Part 2:', combos_for_min_size(containers, 150))
