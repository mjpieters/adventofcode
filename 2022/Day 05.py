import re
from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, Self

import aocd


@dataclass
class Stacks:
    stacks: tuple[deque[str]]

    def __str__(self) -> str:
        stacks = [list(stack) for stack in self.stacks]
        max_height = max(len(stack) for stack in stacks)
        cols = []
        for i, stack in enumerate(stacks, 1):
            if cols:
                cols.append(" " * (max_height + 1))
            padding = " " * (max_height - len(stack))
            cols.append(" " + "[" * len(stack) + padding)
            cols.append(str(i) + "".join(stack) + padding)
            cols.append(" " + "]" * len(stack) + padding)
        lines = ["".join(line) for line in zip(*cols)]
        return "\n".join(lines[::-1])

    @classmethod
    def from_text(cls, text: str) -> Self:
        # drop the number line, reverse, and only keep the letters columns
        lines = [line[1::4] for line in text.splitlines()[-2::-1]]
        stacks = [
            deque(letter for letter in col if letter != " ") for col in zip(*lines)
        ]
        return cls(tuple(stacks))

    @property
    def tops(self) -> str:
        return "".join([stack[-1] for stack in self.stacks])

    def move_crates(self, source: int, target: int, count: int = 1) -> None:
        intermediary: deque[str] = deque()
        sstack, tstack = self.stacks[source], self.stacks[target]
        for _ in range(count):
            intermediary.append(sstack.pop())
        while intermediary:
            tstack.append(intermediary.pop())


_move: re.Pattern[str] = re.compile(
    r"move (?P<count>\d+) from (?P<source>\d+) to (?P<target>\d+)"
)


class CraneMove(NamedTuple):
    count: int
    source: int
    target: int

    def __str__(self) -> str:
        return f"move {self.count} from {self.source + 1} to {self.target + 1}"

    @classmethod
    def from_line(cls, line: str) -> Self:
        match = _move.search(line)
        assert match is not None
        params = {k: int(v) for k, v in match.groupdict().items()}
        params["source"] -= 1
        params["target"] -= 1
        return cls(**params)


@dataclass
class Crane9000Moves:
    moves: list[CraneMove]

    def __str__(self) -> str:
        return "\n".join([str(move) for move in self.moves])

    @classmethod
    def from_text(cls, text: str) -> Self:
        return cls([CraneMove.from_line(line) for line in text.splitlines()])

    def rearrange(self, stacks: Stacks):
        for move in self.moves:
            for _ in range(move.count):
                stacks.move_crates(move.source, move.target)


example: str = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

test_stacks = Stacks.from_text(example.partition("\n\n")[0])
Crane9000Moves.from_text(example.partition("\n\n")[-1]).rearrange(test_stacks)
assert test_stacks.tops == "CMZ"


starting_positions, _, procedure = aocd.get_data(day=5, year=2022).partition("\n\n")

stacks = Stacks.from_text(starting_positions)
crane = Crane9000Moves.from_text(procedure)
crane.rearrange(stacks)
print("Part 1:", stacks.tops)


@dataclass
class Crane9001Moves(Crane9000Moves):
    def rearrange(self, stacks: Stacks):
        for move in self.moves:
            stacks.move_crates(move.source, move.target, move.count)


test_stacks = Stacks.from_text(example.partition("\n\n")[0])
Crane9001Moves.from_text(example.partition("\n\n")[-1]).rearrange(test_stacks)
assert test_stacks.tops == "MCD"


stacks = Stacks.from_text(starting_positions)
crane = Crane9001Moves.from_text(procedure)
crane.rearrange(stacks)
print("Part 2:", stacks.tops)
