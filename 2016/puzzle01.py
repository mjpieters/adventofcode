instructions = '''\
R5, L2, L1, R1, R3, R3, L3, R3, R4, L2, R4, L4, R4, R3, L2, L1, L1, R2, R4,
R4, L4, R3, L2, R1, L4, R1, R3, L5, L4, L5, R3, L3, L1, L1, R4, R2, R2, L1,
L4, R191, R5, L2, R46, R3, L1, R74, L2, R2, R187, R3, R4, R1, L4, L4, L2, R4,
L5, R4, R3, L2, L1, R3, R3, R3, R1, R1, L4, R4, R1, R5, R2, R1, R3, L4, L2,
L2, R1, L3, R1, R3, L5, L3, R5, R3, R4, L1, R3, R2, R1, R2, L4, L1, L1, R3,
L3, R4, L2, L4, L5, L5, L4, R2, R5, L4, R4, L2, R3, L4, L3, L5, R5, L4, L2,
R3, R5, R5, L1, L4, R3, L1, R2, L5, L1, R4, L1, R5, R1, L4, L4, L4, R4, R3,
L5, R1, L3, R4, R3, L2, L1, R1, R2, R2, R2, L1, L1, L2, L5, L3, L1
'''.split()


class Position:
    hori_adjust = [1, 0, -1, 0]  # for all 4 directions
    vert_adjust = [0, 1, 0, -1]  # ditto

    def __init__(self):
        self.x, self.y = 0, 0
        self._direction = 0   # North 0, East 1, South 2, West 3
        self._visited = set()

    def do_step(self, instr):
        rotation = -1 if instr[0] == 'L' else 1
        steps = int(instr[1:].rstrip(','))
        self._direction = (self._direction + rotation) % 4
        for _ in range(steps):
            self.x += self.hori_adjust[self._direction]
            self.y += self.vert_adjust[self._direction]
            if (self.x, self.y) in self._visited:
                return True
            self._visited.add((self.x, self.y))

    def distance(self):
        return abs(self.x) + abs(self.y)


pos = Position()
for inst in instructions:
    if pos.do_step(inst):
        break
print(pos.distance())
