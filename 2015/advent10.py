# --- Day 10: Elves Look, Elves Say ---
from itertools import groupby
from functools import reduce


def looksay(digits):
    return ''.join(['{}{}'.format(len(list(group)), d)
                    for d, group in groupby(digits)])


assert looksay('1') == '11'
assert looksay('11') == '21'
assert looksay('21') == '1211'
assert looksay('1211') == '111221'
assert looksay('111221') == '312211'


if __name__ == '__main__':
    res1 = reduce(lambda prev, i: looksay(prev), range(40), '1321131112')
    print('Part 1:', len(res1))
    # iterate an *additional* 10 times
    res2 = reduce(lambda prev, i: looksay(prev), range(10), res1)
    print('Part 2:', len(res2))
