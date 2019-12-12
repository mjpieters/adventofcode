#!/usr/bin/env python3.6

import os.path
import re

from itertools import chain, islice

HERE = os.path.dirname(os.path.abspath(__file__))


class Display:
    def __init__(self, width=50, height=6):
        self.pixels = [['.'] * width for _ in range(height)]

    def voltage(self):
        return sum(1 for p in chain.from_iterable(self.pixels) if p == '#')

    def rect(self, a, b):
        for row in range(b):
            self.pixels[row][:a] = ['#'] * a

    def rotate_row(self, row, b):
        self.pixels[row] = self.pixels[row][-b:] + self.pixels[row][:-b]

    def rotate_column(self, col, b):
        column = next(islice(zip(*self.pixels), col, None))
        for row, newval in zip(self.pixels, column[-b:] + column[:-b]):
            row[col] = newval

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.pixels])

    _commands = (
        (re.compile(r'rect (\d+)x(\d+)'), rect),
        (re.compile(r'rotate column x=(\d+) by (\d+)'), rotate_column),
        (re.compile(r'rotate row y=(\d+) by (\d+)'), rotate_row),
    )

    def apply_command(self, command):
        for pattern, method in self._commands:
            match = pattern.search(command)
            if match:
                method(self, *(map(int, match.groups())))
                return


def test():
    d = Display(7, 3)

    d.apply_command('rect 3x2')
    assert str(d) == '###....\n###....\n.......'

    d.apply_command('rotate column x=1 by 1')
    assert str(d) == '#.#....\n###....\n.#.....'

    d.apply_command('rotate row y=0 by 4')
    assert str(d) == '....#.#\n###....\n.#.....'

    d.apply_command('rotate column x=1 by 1')
    assert str(d) == '.#..#.#\n#.#....\n.#.....'

    assert d.voltage() == 6


if __name__ == '__main__':
    import sys
    import time
    if '-t' in sys.argv:
        test()
        sys.exit(0)

    animate = '-p' in sys.argv
    d = Display()
    with open(os.path.join(HERE, 'puzzle08_input.txt')) as commands:
        if animate:
            print('\n' * 5)
        for command in commands:
            d.apply_command(command)
            if animate:
                print('\u001b[50D\u001b[7A')
                print(str(d).translate({46: 32, 35: 0x2588}))
                time.sleep(0.05)
    if not animate:
        print('Star 1:', d.voltage())
        print('Star 2:', d, sep='\n')
