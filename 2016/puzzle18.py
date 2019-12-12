from itertools import islice


# set of preceding tile sequences that make a trap in the next row
_is_trap = {
    (True, True, False),
    (False, True, True),
    (True, False, False),
    (False, False, True)
}


def gen_rows(start):
    cache = {}
    yield start
    row = start
    while True:
        if row not in cache:
            previous = (False,) + row + (False,)
            cache[row] = tuple(
                three in _is_trap
                for three in zip(previous, previous[1:], previous[2:]))
        row = cache[row]
        yield row


def count_safe(start, rows):
    return sum(len(row) - sum(row) for row in islice(gen_rows(start), rows))


def row_from_str(row):
    return tuple(tile == '^' for tile in row)


def test():
    print('Star 1 test')
    start = row_from_str('..^^.')
    assert list(islice(gen_rows(start), 3)) == list(map(
        row_from_str,
        ('..^^.', '.^^^^', '^^..^')
    ))
    start = row_from_str('.^^.^.^^^^')
    assert count_safe(start, 10) == 38

    # print('Star 2 test')
    print('Tests passed')


if __name__ == '__main__':
    import sys

    if '-t' in sys.argv:
        test()
        sys.exit(0)

    start = row_from_str(
        '^.....^.^^^^^.^..^^.^.......^^..^^^..^^^^..^.^^.^.'
        '^....^^...^^.^^.^...^^.^^^^..^^.....^.^...^.^.^^.^')
    print('Star 1:', count_safe(start, 40))
    print('Star 2:', count_safe(start, 400000))
