def gendata(start):
    swap = {ord('0'): '1', ord('1'): '0'}
    a = start
    while True:
        a = '{}0{}'.format(a, a[::-1].translate(swap))
        yield a


def checksum(value):
    def combine(a, b):
        return '1' if a == b else '0'

    checksum = value
    while True:
        checksum = ''.join([combine(a, b)
                            for a, b in zip(*([iter(checksum)] * 2))])
        if len(checksum) % 2 == 1:
            return checksum


def filldisk(start, length):
    data = next(filter(lambda d: len(d) >= length, gendata(start)))
    data = data[:length]
    return checksum(data)


def test():
    print('Star 1 test')
    assert next(gendata('1')) == '100'
    assert next(gendata('0')) == '001'
    assert next(gendata('11111')) == '11111000000'
    assert next(gendata('111100001010')) == '1111000010100101011110000'
    assert checksum('110010110100') == '100'
    assert filldisk('10000', 20) == '01100'

    print('Tests passed')


if __name__ == '__main__':
    import sys

    if '-t' in sys.argv:
        test()
        sys.exit(0)

    start = '10001001100000001'

    print('Star 1:', filldisk(start, 272))
    print('Star 2:', filldisk(start, 35651584))
