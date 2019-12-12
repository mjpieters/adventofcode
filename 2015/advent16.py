import os
import operator

HERE = os.path.dirname(os.path.abspath(__file__))

clues = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}


def parse_aunts(fileobj):
    for line in fileobj:
        name, __, props = line.partition(':')
        props = {name.strip(): int(count)
                 for entry in props.split(',')
                 for name, count in (entry.split(':'),)}
        yield name.strip(), props


with open(os.path.join(HERE, 'inputs/input16.txt')) as fileobj:
    aunts = list(parse_aunts(fileobj))

aunt = next(name for name, props in aunts
            if all(props[k] == clues[k]
                   for k in props.keys() & clues.keys()))
print('Part 1:', aunt)

comps = {
    'cats': operator.gt,
    'trees': operator.gt,
    'pomeranians': operator.lt,
    'goldfish': operator.lt,
}
aunt = next(name for name, props in aunts
            if all(comps.get(k, operator.eq)(props[k], clues[k])
                   for k in props.keys() & clues.keys()))
print('Part 2:', aunt)
