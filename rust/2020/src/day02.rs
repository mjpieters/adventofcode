use aoc_runner_derive::{aoc, aoc_generator};
use regex::Regex;
use std::error::Error;
use std::fmt::Display;
use std::str::FromStr;

lazy_static! {
    static ref LINERE: Regex =
        Regex::new(r"^(?P<min>\d+)-(?P<max>\d+)\s*(?P<letter>[a-z]):\s*(?P<password>[a-z]+)$")
            .unwrap();
}

#[derive(Debug)]
struct PWRule {
    min: usize,
    max: usize,
    letter: char,
    password: String,
}

impl PWRule {
    fn is_valid(&self) -> bool {
        let count = self.password.chars().filter(|c| *c == self.letter).count();
        self.min <= count && count <= self.max
    }

    fn is_valid_toboggan_policy(&self) -> bool {
        self.password
            .chars()
            .enumerate()
            .filter(|(i, c)| (*i == self.min - 1 || *i == self.max - 1) && *c == self.letter)
            .count()
            == 1
    }
}

#[derive(Debug)]
struct PWRuleError;

impl Error for PWRuleError {}
impl Display for PWRuleError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Could not parse password rule")
    }
}

impl FromStr for PWRule {
    type Err = PWRuleError;
    fn from_str(line: &str) -> Result<Self, Self::Err> {
        LINERE
            .captures(line)
            .and_then(|cap| {
                Some(PWRule {
                    min: cap.name("min")?.as_str().parse().ok()?,
                    max: cap.name("max")?.as_str().parse().ok()?,
                    letter: cap.name("letter")?.as_str().chars().next()?,
                    password: cap.name("password")?.as_str().into(),
                })
            })
            .ok_or(PWRuleError)
    }
}

#[aoc_generator(day2)]
fn read_pwrules(input: &str) -> Result<Vec<PWRule>, PWRuleError> {
    input.lines().map(|l| l.parse()).collect()
}

#[aoc(day2, part1)]
fn count_valid(pwrules: &Vec<PWRule>) -> usize {
    pwrules.iter().filter(|pwrule| pwrule.is_valid()).count()
}

#[aoc(day2, part2)]
fn count_valid_toboggan(pwrules: &Vec<PWRule>) -> usize {
    pwrules
        .iter()
        .filter(|pwrule| pwrule.is_valid_toboggan_policy())
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    static EXAMPLE: &str = "1-3 a: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc";

    #[test]
    fn test_part1() -> Result<(), PWRuleError> {
        let pwrules = read_pwrules(EXAMPLE)?;
        assert_eq!(count_valid(&pwrules), 2);
        Ok(())
    }

    #[test]
    fn test_part2() -> Result<(), PWRuleError> {
        let pwrules = read_pwrules(EXAMPLE)?;
        assert_eq!(count_valid_toboggan(&pwrules), 1);
        Ok(())
    }
}
