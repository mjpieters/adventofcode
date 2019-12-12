from itertools import product, combinations
from collections import namedtuple
import re

Item = namedtuple('Item', 'name cost damage armour')
conv = lambda n: int(n) if n.isdigit() else n
load = lambda lines: [Item(*map(conv, re.split(r'\s{2,}', l))) for l in lines]

weapons = load('''\
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0
'''.splitlines())

# Armour is optional, include a noop.
armour = load('''\
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
None          0     0       0
'''.splitlines())

# Rings are optional; we pick between 0 and 2 so include 2 noops.
rings = load('''\
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
None          0     0       0
None          0     0       0
'''.splitlines())


def attack(weapon, rings, boss_armour):
    return max(1, weapon.damage + sum(r.damage for r in rings) - boss_armour)


def defence(armour, rings, boss_attack):
    return max(1, boss_attack - armour.armour - sum(r.armour for r in rings))


if __name__ == '__main__':
    import sys
    filename = sys.argv[-1]
    with open(filename) as f:
        boss_hp = int(next(f).rpartition(':')[-1])
        boss_attack = int(next(f).rpartition(':')[-1])
        boss_armour = int(next(f).rpartition(':')[-1])

    player_hp = 100

    min_cost = min(
        weapon.cost + armour.cost + sum(r.cost for r in rings)
        for weapon, armour, rings in product(
            weapons, armour, combinations(rings, 2))
        if (boss_hp // attack(weapon, rings, boss_armour) <=
            player_hp // defence(armour, rings, boss_attack)))
    print('Part 1:', min_cost)

    max_cost = max(
        weapon.cost + armour.cost + sum(r.cost for r in rings)
        for weapon, armour, rings in product(
            weapons, armour, combinations(rings, 2))
        if (boss_hp // attack(weapon, rings, boss_armour) >
            player_hp // defence(armour, rings, boss_attack)))
    print('Part 2:', max_cost)
