use aoc_runner_derive::{aoc, aoc_generator};
use std::collections::BTreeSet;
use std::num::ParseIntError;

#[aoc_generator(day1)]
fn read_changes(input: &str) -> Result<Vec<i32>, ParseIntError> {
    input.lines().map(|l| l.parse()).collect()
}

#[aoc(day1, part1)]
fn part1(changes: &Vec<i32>) -> i32 {
    changes.iter().sum()
}

#[aoc(day1, part2)]
fn part2(changes: &Vec<i32>) -> i32 {
    let mut seen = BTreeSet::new();
    let mut freq = 0;

    seen.insert(freq);

    changes
        .iter()
        .cycle()
        .take_while(|&&change| {
            freq += change;
            seen.insert(freq)
        })
        .count();

    freq
}

#[cfg(test)]
mod tests {
    use super::*;

    static EXAMPLES1: &[&str] = &[
        "+1\n-2\n+3\n+1\n",
        "+1\n+1\n+1\n",
        "+1\n+1\n-2\n",
        "-1\n-2\n-3\n",
    ];

    static EXAMPLES2: &[&str] = &[
        "+1\n-2\n+3\n+1\n",
        "+1\n-1",
        "+3\n+3\n+4\n-2\n-4\n",
        "-6\n+3\n+8\n+5\n-6\n",
        "+7\n+7\n-2\n-7\n-4\n",
    ];

    #[test]
    fn part1_example() -> Result<(), ParseIntError> {
        assert_eq!(part1(&read_changes(&EXAMPLES1[0])?), 3);
        assert_eq!(part1(&read_changes(&EXAMPLES1[1])?), 3);
        assert_eq!(part1(&read_changes(&EXAMPLES1[2])?), 0);
        assert_eq!(part1(&read_changes(&EXAMPLES1[3])?), -6);
        Ok(())
    }

    #[test]
    fn part2_example() -> Result<(), ParseIntError> {
        assert_eq!(part2(&read_changes(&EXAMPLES2[0])?), 2);
        assert_eq!(part2(&read_changes(&EXAMPLES2[1])?), 0);
        assert_eq!(part2(&read_changes(&EXAMPLES2[2])?), 10);
        assert_eq!(part2(&read_changes(&EXAMPLES2[3])?), 5);
        assert_eq!(part2(&read_changes(&EXAMPLES2[4])?), 14);
        Ok(())
    }
}
