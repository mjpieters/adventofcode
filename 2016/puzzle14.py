import re

from functools import reduce
from hashlib import md5
from itertools import count, repeat, islice


def stretchkey(hash, count):
    return reduce(lambda h, i: md5(h.encode('ascii')).hexdigest(),
                  repeat(None, count), hash)


def keystream(salt, start, stretch=0, _cache={}):
    template = bytes(salt + '%d', 'ascii')
    counter = count(start)
    while True:
        index = next(counter)
        if (index, stretch) not in _cache:
            _cache[index, stretch] = stretchkey(
                md5(template % index).hexdigest(), stretch)
        yield index, _cache[index, stretch]


def genkeys(salt, stretch=0, _t=re.compile(r'(.)\1\1')):
    for index, hash in keystream(salt, 0, stretch):
        match = _t.search(hash)
        if match:
            # candidate found, check for pentet in next 1000
            pentet = re.compile(r'({})\1\1\1\1'.format(match.group(1)))
            next1000 = islice(keystream(salt, index + 1, stretch), 1000)
            if any(pentet.search(k) for i, k in next1000):
                yield index, hash


def test():
    print('Star 1 test')
    keys = genkeys('abc')
    assert next(keys)[0] == 39
    assert next(keys)[0] == 92
    assert next(islice(keys, 61, None))[0] == 22728

    print('Star 2 test')
    keys = genkeys('abc', stretch=2016)
    assert next(keys)[0] == 10
    assert next(islice(keys, 62, None))[0] == 22551

    print('Tests passed')



if __name__ == '__main__':
    import sys

    salt = 'cuanljph'

    if '-t' in sys.argv:
        test()
        sys.exit(0)

    keys = genkeys(salt)
    index, key64 = next(islice(keys, 63, None))
    print('Star 1:', index)

    keys = genkeys(salt, stretch=2016)
    index, key64 = next(islice(keys, 63, None))
    print('Star 2:', index)
