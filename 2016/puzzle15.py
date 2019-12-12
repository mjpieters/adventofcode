class Disc(object):
    def __init__(self, num, steps, start):
        # starting point of disk *relative to the starting time*
        # disc num is going to be num steps further by the time a ball released
        # at t0 reaches it.
        self.start = (start + num) % steps
        self.steps = steps

    def __iter__(self):
        pos = self.start
        while True:
            yield pos
            pos = (pos + 1) % self.steps


def solve(discs):
    return next(i for i, dpos in enumerate(zip(*discs)) if not any(dpos))


def test():
    print('Star 1 test')
    discs = [
        Disc(1, 5, 4),
        Disc(2, 2, 1)
    ]
    assert solve(discs) == 5

    print('Tests passed')


if __name__ == '__main__':
    import sys

    if '-t' in sys.argv:
        test()
        sys.exit(0)

    discs = [
        Disc(1, 13, 1),
        Disc(2, 19, 10),
        Disc(3, 3, 2),
        Disc(4, 7, 1),
        Disc(5, 5, 3),
        Disc(6, 17, 5),
    ]
    print('Star 1:', solve(discs))

    discs.append(Disc(7, 11, 0))
    print('Star 2:', solve(discs))
