import re


class CPU(object):
    def __init__(self, program, register_a=0):
        self.registers = {'a': register_a, 'b': 0}
        self.pos = 0
        self.program = program

    def run(self):
        while 0 <= self.pos < len(self.program):
            self.pos = self.execute()
        return self.registers['b']

    def execute(self ):
        op, *args = self.program[self.pos]
        return getattr(self, 'op_' + op)(*args)

    def op_hlf(self, r):
        self.registers[r] >>= 1
        return self.pos + 1

    def op_tpl(self, r):
        self.registers[r] *= 3
        return self.pos + 1

    def op_inc(self, r):
        self.registers[r] += 1
        return self.pos + 1

    def op_jmp(self, offset):
        return self.pos + int(offset)

    def op_jie(self, r, offset):
        return self.pos + (int(offset) if not self.registers[r] % 2 else 1)

    def op_jio(self, r, offset):
        return self.pos + (int(offset) if self.registers[r] == 1 else 1)


if __name__ == '__main__':
    import sys
    filename = sys.argv[-1]

    with open(filename) as f:
        instructions = [re.split(r'[ ,]+', line.strip()) for line in f]

    cpu = CPU(instructions)
    register_b = cpu.run()
    print('Part 1:', register_b)

    cpu = CPU(instructions, 1)
    register_b = cpu.run()
    print('Part 2:', register_b)
