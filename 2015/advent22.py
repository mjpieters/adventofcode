from collections import namedtuple
from functools import reduce
from heapq import heappop, heappush
from itertools import count


class Spell(namedtuple('BaseSpell',
                       'name cost effect turns damage heal armour mana')):
    def __new__(cls, name, cost, effect=False, turns=None, damage=0, heal=0,
                armour=0, mana=0):
        return super().__new__(
            cls, name, cost, effect, turns, damage, heal, armour, mana)


spells = (
    Spell('Magic Missile', 53,  damage=4),
    Spell('Drain',         73,  damage=2, heal=2),
    Spell('Shield',        113, effect=True, turns=6, armour=7),
    Spell('Poison',        173, effect=True, turns=6, damage=3),
    Spell('Recharge',      229, effect=True, turns=5, mana=101),
)


class State(object):
    def __init__(self, hp, mana, boss_hp, boss_damage,
                 mana_spent=0, effects=None, hard=False,
                 parent=None, spell_cast=None):
        self.hp = hp
        self.mana = mana
        self.boss_hp = boss_hp
        self.boss_damage = boss_damage
        self.mana_spent = mana_spent
        self.effects = effects or ()
        self.hard = hard
        self._parent = parent
        self._spell_cast = spell_cast

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        return all(getattr(self, k) == getattr(other, k)
                   for k in vars(self) if k[0] != '_')

    def __hash__(self):
        return reduce(lambda a, b: a ^ hash(b),
                      (v for k, v in vars(self).items() if k[0] != '_'), 0)

    def iter_path(self):
        if self._parent is None:
            return
        yield from self._parent.iter_path()
        yield self._spell_cast

    def process_effects(self, effects, hp, mana, boss_hp):
        remaining_effects = []
        armour = 0  # either Shield is in effect or it is not
        for timer, effect in self.effects:
            hp += effect.heal
            mana += effect.mana
            boss_hp -= effect.damage
            armour = max(armour, effect.armour)
            if timer > 1:
                remaining_effects.append((timer - 1, effect))
        return tuple(remaining_effects), hp, mana, boss_hp, armour

    def boss_turn(self):
        self.effects, self.hp, self.mana, self.boss_hp, armour = (
            self.process_effects(
                self.effects, self.hp, self.mana, self.boss_hp))
        # only if the boss is still alive can they attack!
        if self.boss_hp > 0:
            self.hp -= max(1, self.boss_damage - armour)

    def transitions(self):
        # Player turn first
        effects, hp, mana, boss_hp, __ = self.process_effects(
            self.effects, self.hp - int(self.hard), self.mana, self.boss_hp)
        for spell in spells:
            if spell.cost > mana or any(spell is s for t, s in effects):
                # can't cast spells for which we have no mana or in effect
                continue
            new_state = State(
                hp, mana - spell.cost, boss_hp, self.boss_damage,
                self.mana_spent + spell.cost, effects, hard=self.hard,
                parent=self, spell_cast=spell.name)
            if not spell.effect:
                new_state.hp += spell.heal
                new_state.boss_hp -= spell.damage
            else:
                new_state.effects = new_state.effects + ((spell.turns, spell),)
            # Boss turn next
            new_state.boss_turn()
            # No point in playing a turn that has the player losing
            if new_state.hp > 0:
                yield new_state


def search_a_star(start):
    open_states = {start}
    pqueue = [(0, start)]
    closed_states = set()
    unique = count()
    while open_states:
        current = heappop(pqueue)[-1]
        if current.boss_hp < 1:
            return current
        open_states.remove(current)
        closed_states.add(current)
        for state in current.transitions():
            if state in closed_states or state in open_states:
                continue
            open_states.add(state)
            heappush(pqueue, (state.mana_spent, next(unique), state))


if __name__ == '__main__':
    import sys
    filename = sys.argv[-1]
    with open(filename) as f:
        boss_hp = int(next(f).rpartition(':')[-1])
        boss_attack = int(next(f).rpartition(':')[-1])

    player_hp, player_mana = 50, 500
    start = State(player_hp, player_mana, boss_hp, boss_attack)
    end = search_a_star(start)
    print('Part 1:', end.mana_spent)
    if '-v' in sys.argv:
        print(*end.iter_path(), sep=' -> ')

    start.hard = True
    end = search_a_star(start)
    print('Part 2:', end.mana_spent)
    if '-v' in sys.argv:
        print(*end.iter_path(), sep=' -> ')
