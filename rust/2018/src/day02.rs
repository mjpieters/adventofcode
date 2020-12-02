use aoc_runner_derive::aoc;
use counter::Counter;
use sequence_trie::SequenceTrie;

#[aoc(day2, part1)]
fn checksum(input: &str) -> u32 {
    let (twos, threes) = input.lines().fold((0_u32, 0_u32), |(twos, threes), id| {
        let (count2, count3) = id.chars().collect::<Counter<char>>().values().fold(
            (0_u32, 0_u32),
            |(count2, count3), c| match c {
                2 => (count2 + 1, count3),
                3 => (count2, count3 + 1),
                _ => (count2, count3),
            },
        );
        match (count2, count3) {
            (0, 0) => (twos, threes),
            (1..=u32::MAX, 0) => (twos + 1, count3),
            (0, 1..=u32::MAX) => (twos, count3 + 1),
            (1..=u32::MAX, 1..=u32::MAX) => (twos + 1, count3 + 1),
        }
    });

    twos * threes
}

#[aoc(day2, part2)]
fn matching_ids(input: &str) -> String {
    let mut trie: SequenceTrie<u8, ()> = SequenceTrie::new();
    for id in input.lines() {
        let mut stack: Vec<_> = vec![&trie];
        for (i, byte) in id.as_bytes().iter().enumerate() {
            if i == stack.len() {
                // insert remainder as a new trie entry
                trie.insert(id.as_bytes().iter(), ());
                break;
            }
            let current = stack[i];
            let mut found = None;
            for (tchar, sub) in current.children_with_keys() {
                if *tchar == *byte {
                    // save subnode key for when we can safely mutate the stack.
                    found = Some(tchar);
                } else {
                    // check if there is a full postfix match
                    if sub.get(id.as_bytes().iter().skip(i + 1)).is_some() {
                        return String::from([&id[..i], &id[i + 1..]].concat());
                    };
                };
            }
            if let Some(tchar) = found {
                stack.push(&current.get_node([*tchar].iter()).unwrap());
            };
        }
    }
    unreachable!("No solution!")
}

#[cfg(test)]
mod tests {
    use super::*;

    static EXAMPLE1: &str = "abcdef\nbababc\nabbcde\nabcccd\naabcdd\nabcdee\nababab";
    static EXAMPLE2: &str = "abcde\nfghij\nklmno\npqrst\nfguij\naxcye\nwvxyz";

    #[test]
    fn part1_example() {
        assert_eq!(checksum(&EXAMPLE1), 12);
    }

    #[test]
    fn part2_example() {
        assert_eq!(matching_ids(&EXAMPLE2), "fgij");
    }
}
