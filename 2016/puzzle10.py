import os.path
import re
from collections import deque


HERE = os.path.dirname(os.path.abspath(__file__))


def create_bot(source, low, high):
    def bot(namespace):
        chips = namespace.get(source)
        if chips is not None and len(chips) > 1:
            return {high: max(chips), low: min(chips)}
    bot.__qualname__ = source
    return bot


_input = re.compile('value (\d+) goes to ((?:bot|output) \d+)')
_bot = re.compile('(bot \d+) gives low to ((?:bot|output) \d+) '
                  'and high to ((?:bot|output) \d+)')


def solve(instructions):
    namespace = {}
    bots = deque()
    for instruction in instructions:
        input = _input.search(instruction)
        if input:
            value, target = input.groups()
            namespace.setdefault(target, []).append(int(value))
            continue
        source, low, high = _bot.search(instruction).groups()
        bots.append(create_bot(source, low, high))

    while bots:
        bot = bots.popleft()
        output = bot(namespace)
        if output:
            for target, value in output.items():
                namespace.setdefault(target, []).append(value)
        else:
            bots.append(bot)

    return namespace


def test():
    test_instructions = '''\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
'''.splitlines(True)
    namespace = solve(test_instructions)
    assert namespace['output 0'] == [5]
    assert namespace['output 1'] == [2]
    assert namespace['output 2'] == [3]


if __name__ == '__main__':
    import sys
    if '-t' in sys.argv:
        test()
        sys.exit(0)

    with open(os.path.join(HERE, 'puzzle10_input.txt'), 'r') as instructions:
        namespace = solve(instructions)

    botname = next(target for target, chips in namespace.items()
                   if set(chips) == {17, 61})
    print('Star 1:', botname)
    out1, out2, out3 = (namespace['output {}'.format(i)][0] for i in range(3))
    print('Star 2:', out1 * out2 * out3)
