import re
from itertools import takewhile
from random import shuffle


def one_step_substitute(molecule, replacements):
    for i, atom in enumerate(molecule):
        for subst in replacements.get(atom, []):
            yield ''.join(molecule[:i] + [subst] + molecule[i + 1:])


def random_replace(molecule, replacements):
    # to hell with finding the right order of substitutions by analysis;
    # there is only one solution and the *quickest* way to that solution
    # is trying out random substition orderings.
    molecule = ''.join(molecule)
    reversed = [(v, k) for k in replacements for v in replacements[k]]
    steps = 0
    target = molecule
    while target != 'e':
        changed = False
        for repl, source in reversed:
            if repl in target:
                target = target.replace(repl, source, 1)
                steps += 1
                changed = True
        if not changed:
            target = molecule
            shuffle(reversed)
            steps = 0
    return steps


def read_input(fileobj, _atom=re.compile('[A-Z][a-z]*')):
    fileobj = iter(fileobj)
    replacements = {}
    for line in takewhile(lambda l: l.strip(), fileobj):
        source, __, target = line.strip().partition(' => ')
        replacements.setdefault(source, []).append(target)
    molecule = next(fileobj).strip()
    return replacements, _atom.findall(molecule)


if __name__ == '__main__':
    import sys
    filename = sys.argv[-1]
    with open(filename) as f:
        replacements, molecule = read_input(f)
    count = len(set(one_step_substitute(molecule, replacements)))
    print('Part 1:', count)

    steps = random_replace(molecule, replacements)
    print('Part 2:', steps)
