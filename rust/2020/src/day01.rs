use aoc_runner_derive::{aoc, aoc_generator};
use std::collections::HashSet;
use std::num::ParseIntError;

#[aoc_generator(day1)]
fn read_coins(input: &str) -> Result<HashSet<i32>, ParseIntError> {
    input.lines().map(|l| l.parse()).collect()
}

fn find_sum(coins: &HashSet<i32>, target: i32) -> Option<(i32, i32)> {
    for first in coins {
        let second = target.wrapping_sub(*first);
        if coins.contains(&second) {
            return Some((*first, second));
        }
    }
    None
}

#[aoc(day1, part1)]
fn part1(coins: &HashSet<i32>) -> i32 {
    if let Some((first, second)) = find_sum(coins, 2020) {
        return first * second;
    }
    unreachable!("No solution!")
}

#[aoc(day1, part2)]
fn part2(coins: &HashSet<i32>) -> i32 {
    for selected in coins {
        if let Some((first, second)) = find_sum(coins, 2020_i32.wrapping_sub(*selected)) {
            return selected * first * second;
        }
    }
    unreachable!("No solution!");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1_example() {
        let example: HashSet<i32> = vec![1721, 979, 366, 299, 675, 1456].into_iter().collect();
        assert_eq!(part1(&example), 514579);
    }
    #[test]
    fn part2_example() {
        let example: HashSet<i32> = vec![1721, 979, 366, 299, 675, 1456].into_iter().collect();
        assert_eq!(part2(&example), 241861950);
    }
}
