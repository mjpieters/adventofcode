def josephus(elves):
    # Rotate binary value by 1 (MSB to LSB) for an O(logN) answer (basically
    # counting the bits in N, then shifting them in logN steps)
    size = elves.bit_length()
    mask = (1 << size) - 1
    return (elves << 1 & mask) + (elves >> size - 1)


class ElfNode:
    # slots to avoid costly memory allocations, saves seconds of the
    # runtime.
    # We can save a little more time still by inlining __init__ and remove
    # but that makes the code also harder to follow.
    __slots__ = ('next_', 'num')

    def __init__(self, num):
        self.num = num

    def remove(self):
        # not really remove, remove the *next* node instead by
        # copying the state of the next to this
        self.num, self.next_ = self.next_.num, self.next_.next_


def elves_elimination(count):
    head = node = mid = ElfNode(1)
    midnum = count // 2 + 1
    for num in range(2, count + 1):
        node.next_ = node = ElfNode(num)
        if num == midnum:
            mid = node
    # close the circle
    node.next_ = head
    # clean up; only mid remains
    del head, node

    for i in range(count, 1, -1):
        mid.remove()
        # mid is automatically promoted to the next element
        # however, on an odd number of elves remaining, it's the elf to their
        # left that gets the chop instead.
        if i % 2:
            mid = mid.next_

    return mid.num


def test():
    print('Star 1 test')
    assert josephus(5) == 3

    print('Star 2 test')
    assert elves_elimination(5) == 2
    print('Tests passed')


if __name__ == '__main__':
    import sys

    if '-t' in sys.argv:
        test()
        sys.exit(0)

    count = 3014387
    print('Star 1:', josephus(count))
    print('Star 2:', elves_elimination(count))
