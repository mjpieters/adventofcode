import os.path


HERE = os.path.dirname(os.path.abspath(__file__))


def read_number(b, terminator):
    pos = 0
    while pos < len(b) and b[pos] != terminator:
        pos += 1
    return int(b[:pos].tobytes()), pos + 1


def decompress_length(b, version=1):
    b = memoryview(b)
    pos = 0
    while pos < len(b):
        if b[pos] != 40:  # (
            yield 1
            pos += 1
            continue
        length, delta = read_number(b[pos + 1:], 120)  # x
        pos += delta + 1
        count, delta = read_number(b[pos:], 41)  # )
        pos += delta
        if version == 1:
            yield count * length
        else:
            yield count * sum(decompress_length(b[pos:pos + length], version))
        pos += length


def test():
    tests = {
        b'ADVENT': (1, len('ADVENT')),
        b'A(1x5)BC': (1, len('ABBBBBC')),
        b'(3x3)XYZ': (1, len('XYZXYZXYZ')),
        b'A(2x2)BCD(2x2)EFG': (1, len('ABCBCDEFEFG')),
        b'(6x1)(1x3)A': (1, len('(1x3)A')),
        b'X(8x2)(3x3)ABCY': (1, len('X(3x3)ABC(3x3)ABCY')),
        b'(3x3)XYZ': (2, len('XYZXYZXYZ')),
        b'X(8x2)(3x3)ABCY': (2, len('XABCABCABCABCABCABCY')),
        b'(27x12)(20x12)(13x14)(7x10)(1x12)A': (2, 241920),
        b'(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN': (2, 445),
    }
    for test, (version, expected) in tests.items():
        result = sum(decompress_length(test, version))
        assert result == expected, (test, expected, result)


if __name__ == '__main__':
    import sys
    if '-t' in sys.argv:
        test()
        sys.exit(0)

    with open(os.path.join(HERE, 'puzzle09_input.txt'), 'rb') as dataf:
        data = dataf.read().rstrip()

    length = sum(decompress_length(data))
    print('Star 1:', length)

    length = sum(decompress_length(data, 2))
    print('Star 2:', length)
