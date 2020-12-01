use aoc_runner_derive::{aoc, aoc_generator};
use bit_set::BitSet;
use std::collections::BTreeSet;
use std::num::ParseIntError;

#[aoc_generator(day1)]
fn read_coins(input: &str) -> Result<BTreeSet<u32>, ParseIntError> {
    input.lines().map(|l| l.parse()).collect()
}

fn find_sum(coins: &BTreeSet<u32>, target: u32) -> Option<(u32, u32)> {
    for first in coins {
        let second = target.wrapping_sub(*first);
        if coins.contains(&second) {
            return Some((*first, second));
        }
    }
    None
}

#[aoc(day1, part1)]
fn part1(coins: &BTreeSet<u32>) -> u32 {
    if let Some((first, second)) = find_sum(coins, 2020) {
        return first * second;
    }
    unreachable!("No solution!")
}

#[aoc(day1, part2)]
fn part2(coins: &BTreeSet<u32>) -> u32 {
    for selected in coins {
        if let Some((first, second)) = find_sum(coins, 2020_u32.wrapping_sub(*selected)) {
            return selected * first * second;
        }
    }
    unreachable!("No solution!");
}

// BitSet versions

#[aoc_generator(day1, None, BitSet)]
fn read_bitarray(input: &str) -> Result<BitSet<u32>, ParseIntError> {
    input.lines().map(|l| l.parse()).collect()
}

fn find_sum_bitset(coins: &BitSet<u32>, target: usize) -> Option<(usize, usize)> {
    for first in coins {
        let second = target.wrapping_sub(first);
        if coins.contains(second) {
            return Some((first, second));
        }
    }
    None
}

#[aoc(day1, part1, BitSet)]
fn part1_bitset(coins: &BitSet<u32>) -> usize {
    if let Some((first, second)) = find_sum_bitset(&coins, 2020) {
        return first * second;
    };
    unreachable!("No solution!");
}

#[aoc(day1, part2, BitSet)]
fn part2_bitset(coins: &BitSet<u32>) -> usize {
    for selected in coins {
        if let Some((first, second)) = find_sum_bitset(&coins, 2020_usize.wrapping_sub(selected)) {
            return selected * first * second;
        }
    }
    unreachable!("No solution!");
}

#[cfg(test)]
mod tests {
    use super::*;

    static EXAMPLE: &str = "1721\n979\n366\n299\n675\n1456";

    #[test]
    fn test_part2() -> Result<(), ParseIntError> {
        let coins = read_coins(EXAMPLE)?;
        assert_eq!(part1(&coins), 514579);
        Ok(())
    }

    #[test]
    fn test_part1() -> Result<(), ParseIntError> {
        let coins = read_coins(EXAMPLE)?;
        assert_eq!(part2(&coins), 241861950);
        Ok(())
    }

    #[test]
    fn test_part1_bitset() -> Result<(), ParseIntError> {
        let coins = read_bitarray(EXAMPLE)?;
        assert_eq!(part1_bitset(&coins), 514579);
        Ok(())
    }

    #[test]
    fn test_part2_bitset() -> Result<(), ParseIntError> {
        let coins = read_bitarray(EXAMPLE)?;
        assert_eq!(part2_bitset(&coins), 241861950);
        Ok(())
    }
}
