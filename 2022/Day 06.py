from collections import deque, Counter
from itertools import islice
from typing import Iterable

import aocd


def find_n_unique(stream: Iterable[str], n: int = 4) -> int:
    values = iter(stream)
    buffer = deque(islice(values, n), maxlen=n)
    counts = Counter(buffer)
    if all(v == 1 for v in counts.values()):
        return n
    for i, value in enumerate(values, n + 1):
        counts[buffer[0]] -= 1
        counts[value] += 1
        counts += Counter()  # clear zeros and empty values
        if len(counts) == n:
            return i
        buffer.append(value)


part1_tests = {
    "bvwbjplbgvbhsrlpgdmjqwftvncz": 5,
    "nppdvjthqldpwncqszvftbrmjlhg": 6,
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11,
}
for test, expected in part1_tests.items():
    result = find_n_unique(test)
    assert result == expected, f"{test}: {result} != {expected}"


datastream = aocd.get_data(day=6, year=2022)
print("Part 1:", find_n_unique(datastream))


part2_tests = {
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 19,
    "bvwbjplbgvbhsrlpgdmjqwftvncz": 23,
    "nppdvjthqldpwncqszvftbrmjlhg": 23,
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 29,
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 26,
}
for test, expected in part2_tests.items():
    result = find_n_unique(test, 14)
    assert result == expected, f"{test}: {result} != {expected}"

print("Part 2:", find_n_unique(datastream, 14))
