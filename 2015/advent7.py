import operator
import re


class Expression(object):
    _ops = {
        'AND': operator.and_,
        'OR': operator.or_,
        'NOT': lambda x, y: ~y & 0xFFFF,  # bitwise inversion, only one operand
        'LSHIFT': lambda x, y: (x << y) & 0xFFFF,
        'RSHIFT': operator.rshift,
        None: lambda x, y: x,  # direct assignment, only one operand
    }

    _line = re.compile(
        r'(?:(?P<op1>[a-z]+|\d+) )?(?:(?P<operator>{}) (?P<op2>[a-z]+|\d+) )?'
        r'-> (?P<target>[a-z]+)'.format(
            '|'.join([k for k in _ops if k is not None])))

    def __init__(self, op1, operator, op2, target):
        self.op1 = int(op1) if op1 and op1.isdigit() else op1
        self.op2 = int(op2) if op2 and op2.isdigit() else op2
        self.op_name = operator
        self.operator = self._ops[operator]
        self.target = target

    @classmethod
    def from_line(cls, line):
        match = cls._line.search(line)
        if not match:
            raise ValueError('not a valid expression')
        return cls(**match.groupdict())

    def __repr__(self):
        return (
            '{}("{s.op1!r} {s.op_name!r} {s.op2!r} -> {s.target!r}")'.format(
                type(self).__name__, s=self))

    def __call__(self, expressions, _cache):
        if self.target in _cache:
            return _cache[self.target]
        op1, op2 = (
            expressions[op](expressions, _cache) if isinstance(op, str) else op
            for op in (self.op1, self.op2))
        res = _cache[self.target] = self.operator(op1, op2)
        return res


class Solver(object):
    def __init__(self):
        # target -> expression. All targets are unique
        self.expressions = {}

    def parse_instruction(self, line):
        expr = Expression.from_line(line)
        self.expressions[expr.target] = expr

    def solve(self, target='a'):
        return self.expressions[target](self.expressions, {})

    def to_dot_graph(self, output):
        with open(output, 'w') as df:
            df.write('digraph advent_expression {\n')
            for node in self.expressions.values():
                df.write(
                    'n{0} [shape=box,label="{0}"]\n'
                    'n{0}_expr [shape=plaintext,label="{1}"]\n'
                    'n{0} -> n{0}_expr\n'.format(
                        node.target, node.op_name or '='))
                for label, op in (('l', node.op1), ('r', node.op2)):
                    if op is None:
                        continue
                    if isinstance(op, int):
                        # Numbers are repeated
                        df.write(
                            'n{0}{1} [shape=circle,label="{1}"]\n'
                            'n{0}_expr -> n{0}{1} [label="{2}"]\n'.format(
                                node.target, op, label))
                    else:
                        df.write('n{0}_expr -> n{1} [label="{2}"]\n'.format(
                            node.target, op, label))
            df.write('}\n')


if __name__ == '__main__':
    import sys
    import os.path

    filename = sys.argv[-1]

    solver = Solver()
    with open(filename) as inputfile:
        for line in inputfile:
            solver.parse_instruction(line)
    result = solver.solve()
    print('Part 1:', result)

    if '--graph' in sys.argv:
        dirname, base = os.path.split(filename)
        output = os.path.join(
            dirname, os.path.splitext(base)[0] + '.dot')
        solver.to_dot_graph(output)
        print('Saved graph to', output)

    solver.expressions['b'].op1 = result
    print('Part 2:', solver.solve())
