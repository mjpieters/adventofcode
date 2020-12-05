use aoc_runner_derive::{aoc, aoc_generator};
use itertools::Itertools;
use std::collections::BTreeSet;
use std::error::Error;
use std::fmt::{Debug, Display};
use std::str::FromStr;

#[derive(PartialEq, Eq, PartialOrd, Ord)]
struct SeatId {
    pub id: u16,
    pub row: u8,
    pub col: u8,
}

impl SeatId {
    fn new(id: u16) -> Self {
        Self {
            id: id & 1023,
            row: ((id >> 3) & 127) as u8,
            col: (id & 7) as u8,
        }
    }
}

impl Debug for SeatId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let rowid = format!("{:07b}", self.row)
            .replace("0", "F")
            .replace("1", "B");
        let colid = format!("{:03b}", self.col)
            .replace("0", "L")
            .replace("1", "R");
        f.write_fmt(format_args!("<SeatId {} {}-{}>", self.id, rowid, colid))
    }
}

#[derive(Debug)]
struct BoardingPassParseError;

impl Display for BoardingPassParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("Not a valid boarding pass")
    }
}

impl Error for BoardingPassParseError {}

impl FromStr for SeatId {
    type Err = BoardingPassParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.len() {
            10 => s.char_indices().fold(Ok(0), |acc, (i, c)| match acc {
                Ok(id) => match (i, c) {
                    (0..=6, 'F') | (7..=9, 'L') => Ok(id << 1),
                    (0..=6, 'B') | (7..=9, 'R') => Ok((id << 1) | 1),
                    _ => Err(BoardingPassParseError),
                },
                _ => acc,
            }),
            _ => Err(BoardingPassParseError),
        }
        .and_then(|id| Ok(SeatId::new(id)))
    }
}

#[aoc_generator(day5)]
fn parse_boardingpasses(input: &str) -> Result<Vec<SeatId>, BoardingPassParseError> {
    input.lines().map(|l| l.parse()).collect()
}

#[aoc(day5, part1)]
fn max_seatid(seatids: &Vec<SeatId>) -> u16 {
    seatids.iter().max().unwrap().id
}

#[aoc(day5, part2)]
fn find_empty(seatids: &Vec<SeatId>) -> u16 {
    let minid: u16 = (u16::from(seatids.iter().map(|s| s.row).min().unwrap()) << 3) & 7;
    let maxid: u16 = u16::from(seatids.iter().map(|s| s.row).max().unwrap()) << 3;
    let occupied: BTreeSet<_> = seatids.iter().map(|s| s.id).collect();

    (minid..maxid)
        .tuple_windows()
        .filter_map(|(b, s, a)| {
            match (
                occupied.contains(&b),
                occupied.contains(&s),
                occupied.contains(&a),
            ) {
                (true, false, true) => Some(s),
                _ => None,
            }
        })
        .next()
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    static EXAMPLES: [(&str, u8, u8, u16); 4] = [
        ("FBFBBFFRLR", 44, 5, 357),
        ("BFFFBBFRRR", 70, 7, 567),
        ("FFFBBBFRRR", 14, 7, 119),
        ("BBFFBBFRLL", 102, 4, 820),
    ];

    #[test]
    fn test_seatids() -> Result<(), BoardingPassParseError> {
        let mut seatids: Vec<SeatId> = vec![];
        for (pass, row, col, id) in EXAMPLES.iter() {
            let seatid: SeatId = pass.parse()?;
            assert_eq!(seatid.row, *row);
            assert_eq!(seatid.col, *col);
            assert_eq!(seatid.id, *id);
            seatids.push(seatid);
        }
        println!("Seat IDs: {:?}", seatids);
        assert_eq!(
            seatids.iter().max().unwrap().id,
            *EXAMPLES.iter().map(|(.., id)| id).max().unwrap()
        );
        Ok(())
    }
}
