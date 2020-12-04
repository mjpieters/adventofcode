use aoc_runner_derive::aoc;

fn count_trees(map: &str, right: usize, down: usize) -> u32 {
    let cols = (0..).step_by(right);
    map.lines()
        .step_by(down)
        .zip(cols)
        .map(|(row, c)| {
            let col = c % row.len();
            if row[col..=col] == *"#" {
                1_u32
            } else {
                0_u32
            }
        })
        .sum()
}

fn test_slopes(map: &str) -> u32 {
    let slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)];
    slopes
        .iter()
        .map(|(right, down)| count_trees(map, *right, *down))
        .product()
}

#[aoc(day3, part1)]
fn part1(map: &str) -> u32 {
    count_trees(map, 3, 1)
}

#[aoc(day3, part2)]
fn part2(map: &str) -> u32 {
    test_slopes(map)
}

#[cfg(test)]
mod tests {
    use super::*;

    static EXAMPLE: &str = "\
        ..##.......\n\
        #...#...#..\n\
        .#....#..#.\n\
        ..#.#...#.#\n\
        .#...##..#.\n\
        ..#.##.....\n\
        .#.#.#....#\n\
        .#........#\n\
        #.##...#...\n\
        #...##....#\n\
        .#..#...#.#\n\
    ";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&EXAMPLE), 7);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&EXAMPLE), 336);
    }
}
