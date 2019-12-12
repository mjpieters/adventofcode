# Travelling salesm^WSanta.
# Just bruteforce it; it's only 7!
import re
from itertools import permutations


def shortest(g):
    return min(
        sum(g[a][b] for a, b in zip(path, path[1:]))
        for path in permutations(g))


def longest(g):
    return max(
        sum(g[a][b] for a, b in zip(path, path[1:]))
        for path in permutations(g))


def read_graph(fileobj):
    parse_line = re.compile(r'(\w+) to (\w+) = (\d+)')
    g = {}
    for line in fileobj:
        m = parse_line.search(line)
        if not m:
            continue
        from_, to, dist = m.groups()
        g.setdefault(from_, {})[to] = int(dist)
        g.setdefault(to, {})[from_] = int(dist)
    return g


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    with open(filename) as f:
        g = read_graph(f)
    print('Part 1:', shortest(g))
    print('Part 2:', longest(g))
