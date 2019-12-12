import os.path
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import puzzle12  # noqa


class ExtendedBunnyProc(puzzle12.BunnyProc):
    def execute(self, assembunny):
        self._patched_regions = {}
        super().execute(assembunny)

    def _clear_region(self, target):
        to_clear = []
        for pos, orig in self._patched_regions.items():
            if pos <= target < pos + len(orig):
                self.assembunny[pos:pos + len(orig)] = orig
                to_clear.append(pos)
        for pos in to_clear:
            del self._patched_regions[pos]

    def _test_patch(self):
        # peek ahead and see if we entered a multiplication or addition loop
        p = self.assembunny[self.pos:self.pos + 5]
        instr, op1, op2 = zip(*((i + [None])[:3] for i in p))
        if (instr == ('inc', 'dec', 'jnz', 'dec', 'jnz') and
                (op2[2], op2[4]) == ('-2', '-5') and
                op1[0] not in op1[1:] and
                op1[1] == op1[2] and
                op1[3] == op1[4]):
            self._patched_regions[self.pos] = p
            self.assembunny[self.pos:self.pos + 1] = [
                ['mul', op1[0], op1[1], op1[3]],
            ]
            return True
        elif (instr[:3] == ('dec', 'inc', 'jnz') and op2[2] == '-2' and
                (op1[0] == op1[2] != op1[1])):
            self._patched_regions[self.pos] = p[:3]
            self.assembunny[self.pos:self.pos + 1] = [
                ['add', op1[1], op1[0]],
            ]
            return True

    def op_mul(self, x, y, z):
        # optimised operation, multitiply y and z, add to x. Resets y and z.
        self.registers[x] += self.register_or_int(y) * self.register_or_int(z)
        self.registers[y] = self.registers[z] = 0
        self.pos += 5

    def op_add(self, x, y):
        # optimised operation, add y to x. Resets y.
        self.registers[x] += self.register_or_int(y)
        self.registers[y] = 0
        self.pos += 3

    def op_inc(self, x):
        if self._test_patch():
            return
        super().op_inc(x)

    def op_dec(self, x):
        if self._test_patch():
            return
        super().op_dec(x)

    def op_tgl(self, x):
        map_ = {
            'cpy': 'jnz',
            'inc': 'dec',
            'dec': 'inc',
            'jnz': 'cpy',
            'tgl': 'inc',
        }
        target = self.pos + self.register_or_int(x)
        self._clear_region(target)
        try:
            instr, *op = self.assembunny[target]
        except IndexError:
            pass
        else:
            self.assembunny[target] = [map_[instr], *op]
        self.pos += 1


def test():
    print('Star 1 test')
    proc = ExtendedBunnyProc()
    proc.execute('''\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
'''.splitlines(True))
    assert proc.registers['a'] == 3

    # print('Star 2 test')
    print('Tests passed')


if __name__ == '__main__':
    if '-t' in sys.argv:
        test()
        sys.exit(0)

    instructions = '''\
cpy a b
dec b
cpy a d
cpy 0 a
cpy b c
inc a
dec c
jnz c -2
dec d
jnz d -5
dec b
cpy b c
cpy c d
dec d
inc c
jnz d -2
tgl c
cpy -16 c
jnz 1 c
cpy 89 c
jnz 84 d
inc a
inc d
jnz d -2
inc c
jnz c -5
'''.splitlines()

    proc = ExtendedBunnyProc()
    proc.execute(['cpy 7 a'] + instructions)
    print('Star 1:', proc.registers['a'])

    proc = ExtendedBunnyProc()
    proc.execute(['cpy 12 a'] + instructions)
    print('Star 2:', proc.registers['a'])
