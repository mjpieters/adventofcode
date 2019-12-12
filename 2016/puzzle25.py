import os.path
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import puzzle23  # noqa


class OscillatorBunnyProc(puzzle23.ExtendedBunnyProc):
    def _test_patch(self):
        # peek ahead and see if we entered a division or subtraction loop
        p = self.assembunny[self.pos:self.pos + 7]
        instr, op1, op2 = zip(*((i + [None])[:3] for i in p))
        if (instr == ('jnz', 'jnz', 'dec', 'dec',
                      'jnz', 'inc', 'jnz') and
                op2 == ('2', '6', None, None, '-4', None, '-7') and
                op1[0] == op1[2] and op1[3] == op1[4]):
            self._patched_regions[self.pos] = p
            self.assembunny[self.pos:self.pos + 1] = [
                ['div', op1[5], op1[0], op1[3]],
            ]
            return True

        return super()._test_patch()

    def op_div(self, a, b, c):
        # optimised operation, divide b by c, add result to a,
        # leave remainder c or set it to original value
        b_val, c_val = self.register_or_int(b), self.register_or_int(c)
        self.registers[a] += b_val // c_val
        self.registers[c] = (b_val % c_val) or c_val
        self.pos += 7

    def op_jnz(self, x, y):
        if self._test_patch():
            return
        super().op_jnz(x, y)

    def op_out(self, x):
        print(self.register_or_int(x))
        self.pos += 1


if __name__ == '__main__':
    assembunny = '''\
cpy a d
cpy 7 c
cpy 362 b
inc d
dec b
jnz b -2
dec c
jnz c -5
cpy d a
jnz 0 0
cpy a b
cpy 0 a
cpy 2 c
jnz b 2
jnz 1 6
dec b
dec c
jnz c -4
inc a
jnz 1 -7
cpy 2 b
jnz c 2
jnz 1 4
dec b
dec c
jnz 1 -4
jnz 0 0
out b
jnz a -19
jnz 1 -21
'''.splitlines()

    start_value = int(assembunny[1].split()[1]) * int(assembunny[2].split()[1])
    bit_count = start_value.bit_length()
    target = 1
    for _ in range((bit_count // 2) - 1):
        target = (target << 2) | 1

    if bit_count % 2 == 0:
        target = target << 1

    print('Star 1:', target - start_value)

    import sys
    if '-o' in sys.argv:
        proc = OscillatorBunnyProc()
        proc.registers['a'] = target - start_value
        proc.execute(assembunny)
