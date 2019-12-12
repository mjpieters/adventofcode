import os.path

from itertools import chain
from functools import total_ordering


HERE = os.path.dirname(os.path.abspath(__file__))


@total_ordering
class IPRange:
    def __init__(self, start, stop):
        # make stop exclusive, saves on the +1s later on
        self.start, self.stop = start, stop + 1

    def __eq__(self, other):
        return (self.start, self.stop) == (other.start, other.stop)

    def __lt__(self, other):
        return (self.start, self.stop) < (other.start, other.stop)

    def __repr__(self):
        return '<IPRange({0.start}, {0.stop})>'.format(self)


def gaps(ipranges, limit=2**32):
    ranges = iter(ipranges)
    first, second = next(ranges), next(ranges)
    try:
        while True:
            while second.stop <= first.stop:
                second = next(ranges)
            if first.stop < second.start:
                yield range(first.stop, second.start)
            first = second
    except StopIteration:
        if first.stop < limit:
            yield range(first.stop, limit)


def test():
    print('Star 1 test')
    ranges = sorted([IPRange(5, 8), IPRange(0, 2), IPRange(4, 7)])
    assert list(chain.from_iterable(gaps(ranges, 10))) == [3, 9]

    print('Star 2 test')
    assert sum(map(len, gaps(ranges, 10))) == 2

    print('Tests passed')


if __name__ == '__main__':
    import sys

    if '-t' in sys.argv:
        test()
        sys.exit(0)

    ipranges = []
    with open(os.path.join(HERE, 'puzzle20_input.txt'), 'r') as ranges:
        for line in ranges:
            start, stop = map(int, line.split('-'))
            ipranges.append(IPRange(start, stop))
    ipranges.sort()
    print('Star 1:', next(gaps(ipranges))[0])
    print('Star 2:', sum(map(len, gaps(ipranges))))
