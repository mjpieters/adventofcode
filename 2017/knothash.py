from collections import deque
from functools import reduce
from itertools import chain, repeat
from operator import xor

def knot_hash_rounds(lenghts, size=256, rounds=64):
    string = deque(range(size), size)
    skip = pos = 0
    for length in chain.from_iterable(repeat(lenghts, rounds)):
        string.extend(reversed([string.popleft() for _ in range(length)]))
        string.rotate(-skip)
        pos, skip = (pos + length + skip) % size, skip + 1
    string.rotate(pos)
    return list(string)


def knot_hash(value, _suffix=bytes([17, 31, 73, 47, 23])):
    sparse_hash = knot_hash_rounds(value + _suffix)
    dense_hash = bytes(
        reduce(xor, (sparse_hash[b] for b in range(i, i + 16)))
        for i in range(0, 256, 16))
    return dense_hash.hex()
