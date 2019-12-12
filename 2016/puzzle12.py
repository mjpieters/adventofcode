class BunnyProc:
    def __init__(self, print=False):
        self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.pos = 0
        self.print = print

    def execute(self, assembunny):
        self.assembunny = [instruction.split() for instruction in assembunny]
        self.pos = 0
        while self.pos < len(self.assembunny):
            op, *operands = self.assembunny[self.pos]
            getattr(self, 'op_' + op)(*operands)
            if self.print:
                print('\rpos: {0} a: {a} b: {b} c: {c} d: {d}'.format(
                        self.pos, **self.registers),
                      ' ' * 40,
                      end='')

    def register_or_int(self, x):
        return self.registers[x] if x in self.registers else int(x)

    def op_cpy(self, x, y):
        try:
            self.registers[y] = self.register_or_int(x)
        except (KeyError, ValueError):
            pass
        self.pos += 1

    def op_inc(self, x):
        try:
            self.registers[x] += 1
        except KeyError:
            pass
        self.pos += 1

    def op_dec(self, x):
        try:
            self.registers[x] -= 1
        except KeyError:
            pass
        self.pos += 1

    def op_jnz(self, x, y):
        try:
            delta = self.register_or_int(y) if self.register_or_int(x) else 1
            self.pos += delta
        except (KeyError, ValueError):
            self.pos += 1


def test():
    proc = BunnyProc()
    proc.execute('''\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
'''.splitlines(True))
    assert proc.registers['a'] == 42


if __name__ == '__main__':
    import sys
    if '-t' in sys.argv:
        test()
        sys.exit(0)

    instructions = '''\
cpy 1 a
cpy 1 b
cpy 26 d
jnz c 2
jnz 1 5
cpy 7 c
inc d
dec c
jnz c -2
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec d
jnz d -6
cpy 16 c
cpy 17 d
inc a
dec d
jnz d -2
dec c
jnz c -5
'''.splitlines()
    proc = BunnyProc()
    proc.execute(instructions)
    print('Star 1:', proc.registers['a'])

    proc = BunnyProc()
    proc.execute(['cpy 1 c'] + instructions)
    print('Star 2:', proc.registers['a'])
