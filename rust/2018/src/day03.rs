use aoc_runner_derive::{aoc, aoc_generator};
use ranges::{GenericRange, OperationResult, Ranges};
use regex::Regex;
use std::collections::BTreeSet;
use std::error::Error;
use std::fmt::Display;
use std::ops::Bound;
use std::ops::RangeBounds;
use std::str::FromStr;

lazy_static! {
    static ref LINERE: Regex = Regex::new(
        r"#(?P<id>\d+)\s*@\s*(?P<left>\d+),(?P<top>\d+):\s*(?P<width>\d+)x(?P<height>\d+)"
    )
    .unwrap();
}

type ID = usize;

#[derive(Debug)]
struct Rectangle {
    id: ID,
    left: u16,
    right: u16,
    top: u16,
    bottom: u16,
    width: u16,
    height: u16,
    xrange: GenericRange<u16>,
    yrange: GenericRange<u16>,
}

impl Rectangle {
    fn new(id: usize, left: u16, top: u16, width: u16, height: u16) -> Rectangle {
        Rectangle {
            id: id,
            left: left,
            right: left + width,
            top: top,
            bottom: top + height,
            width: width,
            height: height,
            xrange: GenericRange::from(left..(left + width)),
            yrange: GenericRange::from(top..(top + height)),
        }
    }

    fn sum_overlaps(rectangles: &Vec<Self>) -> u32 {
        let max_x = rectangles.iter().map(|r| r.right).max().unwrap();
        (0..max_x)
            .map(|x| {
                // all y ranges for rectangles on the current line
                let mut intervals = rectangles.iter().filter_map(|r| {
                    if r.xrange.contains(&x) {
                        Some(&r.yrange)
                    } else {
                        None
                    }
                });
                let furthest = match intervals.next() {
                    Some(r) => r.to_owned(),
                    None => {
                        return 0;
                    }
                };
                let overlaps: Ranges<_> = intervals
                    .scan(furthest, |furthest, r| {
                        let intersection = match furthest.intersect(*r) {
                            OperationResult::Single(overlap) => overlap,
                            _ => GenericRange::from(0..0),
                        };
                        *furthest = match (r.end_bound(), furthest.end_bound()) {
                            (Bound::Excluded(rend), Bound::Excluded(fend)) if rend > fend => *r,
                            _ => *furthest,
                        };
                        Some(intersection)
                    })
                    .collect();
                overlaps
                    .as_slice()
                    .iter()
                    .map(|r| match (r.start_bound(), r.end_bound()) {
                        (Bound::Included(start), Bound::Excluded(end)) => u32::from(end - start),
                        _ => 0,
                    })
                    .sum()
            })
            .sum()
    }

    fn no_overlaps(rectangles: &Vec<Rectangle>) -> ID {
        let max_x = rectangles.iter().map(|r| r.right).max().unwrap();
        let mut no_overlaps: BTreeSet<ID> = rectangles.iter().map(|r| r.id).collect();
        (0..max_x).for_each(|x| {
            let mut active_rects = rectangles.iter().filter(|&r| r.xrange.contains(&x));
            let mut furthest = match active_rects.next() {
                Some(r) => r.to_owned(),
                None => {
                    return;
                }
            };
            for rect in active_rects {
                if rect.top < furthest.bottom {
                    no_overlaps.remove(&furthest.id);
                    no_overlaps.remove(&rect.id);
                }
                if rect.bottom > furthest.bottom {
                    furthest = rect;
                }
            }
        });
        assert_eq!(no_overlaps.len(), 1);
        *no_overlaps.iter().next().unwrap()
    }
}

#[derive(Debug)]
struct RectangleDefParseError;

impl Error for RectangleDefParseError {}
impl Display for RectangleDefParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Could not parse rectangle definition")
    }
}

impl FromStr for Rectangle {
    type Err = RectangleDefParseError;
    fn from_str(line: &str) -> Result<Self, Self::Err> {
        LINERE
            .captures(line)
            .and_then(|cap| {
                Some(Rectangle::new(
                    cap.name("id")?.as_str().parse().ok()?,
                    cap.name("left")?.as_str().parse().ok()?,
                    cap.name("top")?.as_str().parse().ok()?,
                    cap.name("width")?.as_str().parse().ok()?,
                    cap.name("height")?.as_str().parse().ok()?,
                ))
            })
            .ok_or(RectangleDefParseError)
    }
}

#[aoc_generator(day3)]
fn read_rectangles(input: &str) -> Result<Vec<Rectangle>, RectangleDefParseError> {
    let mut rectangles = input
        .lines()
        .map(|l| l.parse())
        .collect::<Result<Vec<Rectangle>, RectangleDefParseError>>()?;
    rectangles.sort_unstable_by(|a, b| a.top.cmp(&b.top));
    Ok(rectangles)
}

#[aoc(day3, part1)]
fn part1(rectangles: &Vec<Rectangle>) -> u32 {
    Rectangle::sum_overlaps(rectangles)
}

#[aoc(day3, part2)]
fn part2(rectangles: &Vec<Rectangle>) -> ID {
    Rectangle::no_overlaps(rectangles)
}

#[cfg(test)]
mod tests {
    use super::*;

    static TESTRECT: &str = "#123 @ 3,2: 5x4\n";
    static EXAMPLES: [&str; 4] = [
        "#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 5,5: 2x2\n",
        "#1 @ 1,9: 1x9\n#2 @ 1,11: 1x2\n#3 @ 1,15: 1x2\n",
        "#1 @ 1,1: 1x4\n#2 @ 1,3: 1x4\n#3 @ 1,4: 1x5\n",
        "#1 @ 1,1: 1x7\n#2 @ 1,3: 1x6\n#3 @ 1,4: 1x2\n",
    ];

    #[test]
    fn test_parse_rectangle() -> Result<(), RectangleDefParseError> {
        let testrect: Rectangle = TESTRECT.parse()?;
        assert_eq!(
            (testrect.left, testrect.top, testrect.width, testrect.height),
            (3, 2, 5, 4)
        );
        assert_eq!((testrect.right, testrect.bottom), (8, 6));
        assert_eq!(testrect.xrange, GenericRange::from(3..8));
        assert_eq!(testrect.yrange, GenericRange::from(2..6));
        Ok(())
    }

    #[test]
    fn test_part1() -> Result<(), RectangleDefParseError> {
        let test1 = read_rectangles(EXAMPLES[0])?;
        assert_eq!(part1(&test1), 4);
        let test2 = read_rectangles(EXAMPLES[1])?;
        assert_eq!(part1(&test2), 4);
        let test3 = read_rectangles(EXAMPLES[2])?;
        assert_eq!(part1(&test3), 4);
        let test4 = read_rectangles(EXAMPLES[3])?;
        assert_eq!(part1(&test4), 5);
        Ok(())
    }

    #[test]
    fn test_part2() -> Result<(), RectangleDefParseError> {
        let test1 = read_rectangles(EXAMPLES[0])?;
        assert_eq!(part2(&test1), 3);
        Ok(())
    }
}
