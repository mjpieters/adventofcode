import aocd
import string
from typing import Iterator


rucksacks = aocd.get_data(day=3, year=2022).splitlines()


priorities = {letter: i for i, letter in enumerate(string.ascii_letters, 1)}


def misplaced_item(rucksack: str) -> str:
    half = len(rucksack) // 2
    [letter] = set(rucksack[:half]) & set(rucksack[half:])
    return letter


example = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".splitlines()


assert sum(priorities[misplaced_item(r)] for r in example) == 157

print("Part 1:", sum(priorities[misplaced_item(r)] for r in rucksacks))


def badge(rucksack: str, *rucksacks: str) -> str:
    [letter] = set(rucksack).intersection(*rucksacks)
    return letter


def badges(*rucksacks: str) -> Iterator[str]:
    it = iter(rucksacks)
    for group in zip(it, it, it):
        yield badge(*group)


assert sum(priorities[badge] for badge in badges(*example)) == 70

print("Part 2:", sum(priorities[badge] for badge in badges(*rucksacks)))