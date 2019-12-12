from functools import reduce
from itertools import chain, product


def animate(lights):
    new_state = []
    for x, row in enumerate(lights):
        new_state.append([])
        for y, light in enumerate(row):
            count = sum(
                lights[x + dx][y + dy]
                for dx, dy in product(range(-1, 2), repeat=2)
                if (dx or dy) and
                0 <= x + dx < len(lights) and 0 <= y + dy < len(row))
            new_state[-1].append(count in {2, 3} if light else count == 3)
    return new_state


def animate_stuck(lights):
    state = animate(lights)
    state[0][0] = state[0][-1] = state[-1][0] = state[-1][-1] = True
    return state


def read_display(fileobj):
    return [[l == '#' for l in line.strip()] for line in fileobj]


if __name__ == '__main__':
    import sys
    filename = sys.argv[-1]
    with open(filename) as f:
        lights = read_display(f)
    endstate = reduce(lambda l, i: animate(l), range(100), lights)
    result = sum(chain.from_iterable(endstate))
    print('Part 1:', result)

    endstate = reduce(lambda l, i: animate_stuck(l), range(100), lights)
    result = sum(chain.from_iterable(endstate))
    print('Part 2:', result)
