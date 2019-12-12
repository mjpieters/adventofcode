import os.path
HERE = os.path.dirname(os.path.abspath(__file__))


class PadSimple:
    keys = '123456789'
    move_deltas = {'U': -3, 'D': 3, 'L': -1, 'R': 1}
    illegal = {('U', 0, None), ('D', 2, None), ('L', None, 0), ('R', None, 2)}
    legal_moves = {}
    for direction, delta in move_deltas.items():
        for row in range(3):
            for col in range(3):
                if illegal & {(direction, row, None), (direction, None, col)}:
                    continue
                pos = row * 3 + col
                legal_moves[pos, direction] = pos + delta

    def __init__(self):
        self._pos = self.keys.index('5')

    def move(self, instructions):
        for instr in instructions:
            newpos = self.legal_moves.get((self._pos, instr))
            if newpos is not None:
                self._pos = newpos
        return self.keys[self._pos]


class PadConvoluted(PadSimple):
    keys = '123456789ABCD'
    legal_moves = {
        (0, 'D'): 2,
        (1, 'R'): 2, (1, 'D'): 5,
        (2, 'U'): 0, (2, 'R'): 3, (2, 'D'): 6, (2, 'L'): 1,
        (3, 'D'): 7, (3, 'L'): 2,
        (4, 'R'): 5,
        (5, 'U'): 1, (5, 'R'): 6, (5, 'D'): 9, (5, 'L'): 4,
        (6, 'U'): 2, (6, 'R'): 7, (6, 'D'): 10, (6, 'L'): 5,
        (7, 'U'): 3, (7, 'R'): 8, (7, 'D'): 11, (7, 'L'): 6,
        (8, 'L'): 7,
        (9, 'U'): 5, (9, 'R'): 10,
        (10, 'U'): 6, (10, 'R'): 11, (10, 'D'): 12, (10, 'L'): 9,
        (11, 'U'): 7, (11, 'L'): 10,
        (12, 'U'): 10,
    }

    def is_inbounds(self, newpos, samerow=False):
        if not 0 <= newpos < len(self.keys):
            # went off the pad
            return False
        if samerow:
            return (newpos // 3) == self._pos // 3
        return True


def find_bathroom_code(pad, directions):
    code = []
    for line in directions:
        num = pad.move(line.strip())
        code.append(num)
    return ''.join(map(str, code))


sample = '''\
ULL
RRDDD
LURDL
UUUUD
'''

print('Star 1 sample code:',
      find_bathroom_code(PadSimple(), sample.splitlines()))

with open(os.path.join(HERE, 'puzzle02_input.txt')) as input:
    print('Star 1 code:',
          find_bathroom_code(PadSimple(), input))

print('Star 2 sample code:',
      find_bathroom_code(PadConvoluted(), sample.splitlines()))

with open(os.path.join(HERE, 'puzzle02_input.txt')) as input:
    print('Star 2 code:',
          find_bathroom_code(PadConvoluted(), input))
