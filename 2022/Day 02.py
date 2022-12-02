from enum import Enum
from typing import TYPE_CHECKING, Self


class RPS(Enum):
    # value, score, defeats
    rock = "A", 1, "scissors"
    paper = "B", 2, "rock"
    scissors = "C", 3, "paper"

    if TYPE_CHECKING:
        value: str
        score: int
        _defeats: str

    def __new__(cls, value: str, score: int, defeats: str) -> Self:
        instance = object.__new__(cls)
        instance._value_ = value
        instance.score = score
        instance._defeats = defeats
        return instance

    def __gt__(self, other: Self) -> bool:
        """Test if this gesture defeats other"""
        if not isinstance(other, __class__):
            return NotImplemented
        return other.name == self._defeats

    def __str__(self) -> str:
        return self.name.capitalize()


class Outcome(Enum):
    loose = 0
    draw = 3
    win = 6

    @property
    def score(self) -> int:
        return self.value

    @classmethod
    def from_round(cls, opponent: RPS, own: RPS) -> Self:
        if opponent > own:
            return cls.loose
        elif own > opponent:
            return cls.win
        else:
            return cls.draw

    @classmethod
    def score_round(cls, opponent: RPS, own: RPS) -> int:
        return cls.from_round(opponent, own).score + own.score


responses = {"X": RPS.rock, "Y": RPS.paper, "Z": RPS.scissors}
test_input = [line.split() for line in "A Y\nB X\nC Z".splitlines()]
expected_scores = [8, 1, 6]
for (opponent, response), expected in zip(test_input, expected_scores):
    actual = Outcome.score_round(RPS(opponent), RPS(responses[response]))
    assert (
        actual == expected
    ), f"{opponent} vs {response}, expected {expected}, got {actual}"


import aocd

strategy_guide: list[tuple[str, str]] = [
    line.split() for line in aocd.get_data(day=2, year=2022).splitlines()
]

total = sum(
    Outcome.score_round(RPS(opponent), RPS(responses[response]))
    for opponent, response in strategy_guide
)
print("Part 1:", total)

responses = {
    "X": {"A": "C", "B": "A", "C": "B"},
    "Y": {"A": "A", "B": "B", "C": "C"},
    "Z": {"A": "B", "B": "C", "C": "A"},
}

expected_scores = [4, 1, 7]
for (opponent, response), expected in zip(test_input, expected_scores):
    actual = Outcome.score_round(RPS(opponent), RPS(responses[response][opponent]))
    assert (
        actual == expected
    ), f"{opponent} vs {response}, expected {expected}, got {actual}"

total = sum(
    Outcome.score_round(RPS(opponent), RPS(responses[response][opponent]))
    for opponent, response in strategy_guide
)
print("Part 2:", total)
