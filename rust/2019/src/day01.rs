use aoc_runner_derive::{aoc, aoc_generator};
use std::iter::successors;
use std::num::ParseIntError;

#[aoc_generator(day1)]
fn parse_modules(input: &str) -> Result<Vec<u32>, ParseIntError> {
    input.lines().map(|l| l.parse()).collect()
}

#[inline]
fn fuel_requirement(mass: u32) -> u32 {
    (mass / 3).saturating_sub(2)
}

#[inline]
fn iterative_fuel_calc(mass: u32) -> u32 {
    successors(Some(mass), |&m| {
        let requirement = fuel_requirement(m);
        match requirement {
            0 => None,
            _ => Some(requirement),
        }
    })
    .skip(1)
    .sum()
}

#[aoc(day1, part1)]
fn total_fuel(modules: &Vec<u32>) -> u32 {
    modules.iter().map(|&m| fuel_requirement(m)).sum()
}

#[aoc(day1, part2)]
fn total_fuel_iterative(modules: &Vec<u32>) -> u32 {
    modules.iter().map(|&m| iterative_fuel_calc(m)).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    static EXAMPLES1: [(u32, u32); 4] = [(12, 2), (14, 2), (1969, 654), (100756, 33583)];
    static EXAMPLES2: [(u32, u32); 3] = [(14, 2), (1969, 966), (100756, 50346)];

    #[test]
    fn test_fuel_requirement() {
        for (mass, expected) in EXAMPLES1.iter() {
            assert_eq!(fuel_requirement(*mass), *expected);
        }
    }
    #[test]
    fn test_iterative_fuel_calc() {
        for (mass, expected) in EXAMPLES2.iter() {
            assert_eq!(iterative_fuel_calc(*mass), *expected);
        }
    }
}
