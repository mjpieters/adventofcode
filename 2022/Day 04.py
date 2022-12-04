from dataclasses import dataclass
from typing import Self

import aocd


@dataclass
class Assignment:
    start: int
    end: int

    def __str__(self) -> str:
        return f"{self.start}-{self.end}"

    @classmethod
    def from_string(cls, string: str) -> Self:
        start, _, end = string.partition("-")
        return cls(int(start), int(end))

    @classmethod
    def pair_from_line(cls, line: str) -> tuple[Self, Self]:
        p1, _, p2 = line.partition(",")
        return (cls.from_string(p1), cls.from_string(p2))

    def __contains__(self, other: Self) -> bool:
        if not isinstance(other, __class__):
            return NotImplemented
        return (
            self.start <= other.start <= self.end
            and self.start <= other.end <= self.end
        )

    def __and__(self, other: Self) -> bool:
        if not isinstance(other, __class__):
            return NotImplemented
        return not (self.start > other.end or self.end < other.start)


example = [
    Assignment.pair_from_line(line)
    for line in """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".splitlines()
]
assert sum(1 for a1, a2 in example if a1 in a2 or a2 in a1) == 2


assignments = [
    Assignment.pair_from_line(line)
    for line in aocd.get_data(day=4, year=2022).splitlines()
]
print("Part 1:", sum(1 for a1, a2 in assignments if a1 in a2 or a2 in a1))


assert sum(1 for a1, a2 in example if a1 & a2) == 4
print("Part 2:", sum(1 for a1, a2 in assignments if a1 & a2))
