use aoc_runner_derive::{aoc, aoc_generator};
use itertools::Itertools;
use std::collections::BinaryHeap;
use std::error::Error;
use std::fmt;
use std::iter::Sum;
use std::ops::{Add, AddAssign, Neg};
use std::str::FromStr;

type NodeIndex = usize;

#[derive(Debug, Copy, Clone)]
enum Dir {
    Left,
    Right,
}
impl Neg for Dir {
    type Output = Self;

    fn neg(self) -> Self::Output {
        match self {
            Dir::Left => Dir::Right,
            Dir::Right => Dir::Left,
        }
    }
}
impl Add<Dir> for NodeIndex {
    type Output = Self;

    fn add(self, rhs: Dir) -> Self::Output {
        match rhs {
            Dir::Left => self,
            Dir::Right => self + 1,
        }
    }
}
impl PartialEq<Dir> for NodeIndex {
    fn eq(&self, dir: &Dir) -> bool {
        self & 1 == *dir as NodeIndex
    }
}

// compile-time computed constants
const fn factors() -> [u8; 32] {
    let mut factors = [0u8; 32];
    let mut i = 2;
    while i < 32 {
        let mut value = 1;
        let mut node = i as u8;
        while node > 1 {
            value *= 3 - (node & 1);
            node >>= 1;
        }
        factors[i] = value;
        i += 1;
    }
    factors
}
const FACTORS: [u8; 32] = factors();

const fn offsets() -> [NodeIndex; 32] {
    let mut offsets = [0; 32];
    let mut i = 0;
    let mut index = 1;

    while i < 5 {
        let mut n = 0;
        let o: NodeIndex = 2usize.pow(i);
        while n < o {
            offsets[index] = o;
            index += 1;
            n += 1;
        }
        i += 1;
    }
    offsets
}
const OFFSETS: [NodeIndex; 32] = offsets();

// reverse array visiting order for a 32-element tree, used for maintaining a priority queue
const fn visit_order() -> [u8; 32] {
    let mut visit_order = [0; 32];
    let mut node = 1;
    let mut i = 31;
    loop {
        visit_order[node] = i;
        i -= 1;
        node = match node {
            0..=15 => node << 1,
            _ => {
                let mut node = node;
                while node & 1 == 1 {
                    node >>= 1;
                }
                if node == 0 {
                    return visit_order;
                }
                node + 1
            }
        }
    }
}
const VISIT_ORDER: [u8; 32] = visit_order();

#[derive(Debug, PartialEq, Clone, Copy)]
enum TreeNode {
    Unused,
    Branch,
    Leaf(u8),
}
impl PartialEq<u8> for TreeNode {
    fn eq(&self, rhs: &u8) -> bool {
        match self {
            TreeNode::Leaf(lhs) => *lhs == *rhs,
            _ => unreachable!(),
        }
    }
}
impl PartialOrd<u8> for TreeNode {
    fn partial_cmp(&self, rhs: &u8) -> Option<std::cmp::Ordering> {
        match self {
            TreeNode::Leaf(lhs) => lhs.partial_cmp(rhs),
            _ => None,
        }
    }
}
impl AddAssign<u8> for TreeNode {
    fn add_assign(&mut self, rhs: u8) {
        match self {
            TreeNode::Leaf(lhs) => *lhs += rhs,
            _ => unreachable!(),
        }
    }
}

#[derive(Debug)]
struct SnailfishNumber([TreeNode; 32]);

impl SnailfishNumber {
    fn new(btree: [TreeNode; 32]) -> Self {
        Self(btree)
    }

    pub fn magnitude(&self) -> u32 {
        self.into_iter()
            .filter_map(|n| match self.0[n] {
                TreeNode::Leaf(v) => Some(v as u32 * FACTORS[n] as u32),
                TreeNode::Branch => None,
                _ => unreachable!(),
            })
            .sum()
    }
}

#[derive(Debug)]
struct ParseError;

impl Error for ParseError {}
impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Could not parse snailfish number")
    }
}

impl FromStr for SnailfishNumber {
    type Err = ParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut btree = [TreeNode::Unused; 32];
        let mut node: NodeIndex = 1;
        for c in s.chars() {
            node = match c {
                '[' => {
                    btree[node] = TreeNode::Branch;
                    node << 1
                }
                ']' => node >> 1,
                ',' => node + 1,
                '0'..='9' => {
                    btree[node] = TreeNode::Leaf(c as u8 - 0x30);
                    node
                }
                _ => return Err(ParseError),
            };
        }
        Ok(Self::new(btree))
    }
}

// Pre-order traversal iteration over indices to btree nodes
struct SnailfishNumberIter<'s> {
    number: Option<&'s SnailfishNumber>,
    node: NodeIndex,
}

impl<'s> SnailfishNumberIter<'s> {
    fn new(number: &'s SnailfishNumber) -> Self {
        Self {
            number: Some(&number),
            node: 1,
        }
    }
}

impl<'s> Iterator for SnailfishNumberIter<'s> {
    type Item = NodeIndex;

    fn size_hint(&self) -> (usize, Option<usize>) {
        (3, Some(31))
    }

    fn next(&mut self) -> Option<Self::Item> {
        match self.number {
            None => None,
            Some(number) => {
                let node = self.node;
                let result = Some(node);
                self.node = match number.0[node] {
                    TreeNode::Branch => node << 1,
                    TreeNode::Leaf(_) => {
                        let mut node = node;
                        while node == Dir::Right {
                            node = node >> 1;
                        }
                        if node == 0 {
                            self.number = None;
                        }
                        node + 1
                    }
                    _ => unreachable!(),
                };
                result
            }
        }
    }
}

impl<'s> IntoIterator for &'s SnailfishNumber {
    type Item = <SnailfishNumberIter<'s> as Iterator>::Item;
    type IntoIter = SnailfishNumberIter<'s>;

    fn into_iter(self) -> Self::IntoIter {
        Self::IntoIter::new(self)
    }
}

impl fmt::Display for SnailfishNumber {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for node in self {
            match self.0[node] {
                TreeNode::Branch => {
                    write!(f, "[")?;
                }
                TreeNode::Leaf(value) => {
                    write!(f, "{}", value)?;
                    let mut node = node;
                    while node == Dir::Right && node > 1 {
                        node = node >> 1;
                        write!(f, "]")?;
                    }
                    if node == Dir::Left {
                        write!(f, ",")?;
                    }
                }
                _ => unreachable!(),
            };
        }
        Ok(())
    }
}

// Find sibling; if dir is LEFT, preceding, otherwise succeeding
fn find_sibling(btree: &[TreeNode; 32], node: NodeIndex, dir: Dir) -> Option<NodeIndex> {
    let mut node = node;
    while node == dir {
        node >>= 1;
    }
    match node {
        0 | 1 => None, // at or before the root, no sibling
        _ => {
            // move to opposite sibling node at same depth, then go in opposite
            // direction to next leaf
            node = ((node >> 1) << 1) + dir;
            let dir = -dir;
            while let TreeNode::Branch = btree[node] {
                node = node * 2 + dir;
                if node >= 32 {
                    break;
                }
            }
            Some(node)
        }
    }
}

// Binary heap priority queue by traversal order
#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
struct QueuedNode(u8, NodeIndex);
impl From<NodeIndex> for QueuedNode {
    fn from(node: NodeIndex) -> Self {
        Self(VISIT_ORDER[node], node)
    }
}
impl From<QueuedNode> for NodeIndex {
    fn from(node: QueuedNode) -> Self {
        node.1
    }
}

impl<'s, 't> Add<&'t SnailfishNumber> for &'s SnailfishNumber {
    type Output = SnailfishNumber;

    fn add(self, other: &SnailfishNumber) -> Self::Output {
        let mut btree = [TreeNode::Unused; 32];
        let mut pqueue: BinaryHeap<QueuedNode> = BinaryHeap::new();
        let mut overflow = 0u8;

        let mut explode = |btree: &mut [TreeNode; 32], node, l1, l2, pqueue: &mut BinaryHeap<_>| {
            // two new leaves outside the tree, update preceding, succeeding,
            // and parent; the preceding and succeeding nodes are pushed onto
            // the queue, if they need splitting. overflow only applies to the
            // initial copy phase, when exploding can push values to a successor
            // at an index > 32
            btree[node >> 1] = TreeNode::Leaf(0);

            if let Some(prev) = find_sibling(btree, node, Dir::Left) {
                btree[prev] += l1 + overflow;
                overflow = 0;
                if btree[prev] > 9 {
                    pqueue.push(QueuedNode::from(prev));
                }
            };
            if let Some(next) = find_sibling(btree, node + Dir::Right, Dir::Right) {
                if next > 32 {
                    // outside the tree, add to next l1 leaf to explode
                    overflow = l2;
                    return;
                }
                btree[next] += l2;
                if btree[next] > 9 {
                    pqueue.push(QueuedNode::from(next));
                }
            };
        };

        btree[1] = TreeNode::Branch;

        // copy the first 3 levels of the two trees into subtrees on the result
        // add nodes with values over 9 to the queue.
        for i in 1..16 {
            let (ns, vs) = (OFFSETS[i] + i, self.0[i]);
            let (no, vo) = (OFFSETS[i] * 2 + i, other.0[i]);
            btree[ns] = vs;
            btree[no] = vo;
            if vs > 9 {
                pqueue.push(QueuedNode::from(ns));
            }
            if vo > 9 {
                pqueue.push(QueuedNode::from(no));
            }
        }
        // explode the bottom levels of the two trees; first self, then other
        for i in (16..32).step_by(2) {
            if let (TreeNode::Leaf(l1), TreeNode::Leaf(l2)) = (self.0[i], self.0[i + 1]) {
                explode(&mut btree, OFFSETS[i] + i, l1, l2, &mut pqueue);
            }
        }
        for i in (16..32).step_by(2) {
            if let (TreeNode::Leaf(l1), TreeNode::Leaf(l2)) = (other.0[i], other.0[i + 1]) {
                explode(&mut btree, OFFSETS[i] * 2 + i, l1, l2, &mut pqueue);
            }
        }

        // for each entry in the queue:
        // - re-verify that it is still over 9, then split
        // - if split added leaves at level 5, explode (which will queue as needed)
        // - if split values are large enough to need splitting again, add
        //   their nodes to the queue for further checks
        while let Some(queued) = pqueue.pop() {
            let node = NodeIndex::from(queued);
            if let TreeNode::Leaf(value) = btree[node] {
                if value > 9 {
                    btree[node] = TreeNode::Branch;
                    let (l1, l2) = (value / 2, (value + 1) / 2);
                    match node {
                        16..=32 => {
                            explode(&mut btree, node * 2, l1, l2, &mut pqueue);
                        }
                        _ => {
                            btree[node * 2] = TreeNode::Leaf(l1);
                            btree[node * 2 + 1] = TreeNode::Leaf(l2);
                            if l1 > 9 {
                                pqueue.push(QueuedNode::from(node * 2));
                            }
                            if l2 > 9 {
                                pqueue.push(QueuedNode::from(node * 2 + 1));
                            }
                        }
                    }
                }
            }
        }

        SnailfishNumber(btree)
    }
}

impl<'s> Sum<&'s SnailfishNumber> for SnailfishNumber {
    fn sum<I>(mut iter: I) -> SnailfishNumber
    where
        I: Iterator<Item = &'s SnailfishNumber>,
    {
        match iter.next() {
            None => unreachable!(),
            Some(first) => match iter.next() {
                None => unreachable!(),
                Some(second) => iter.fold(first + second, |sum, next| &sum + next),
            },
        }
    }
}

#[aoc_generator(day18)]
fn parse_homework(input: &str) -> Result<Vec<SnailfishNumber>, ParseError> {
    input.lines().map(|line| line.parse()).collect()
}

#[aoc(day18, part1)]
fn sum_numbers(homework: &Vec<SnailfishNumber>) -> u32 {
    homework.iter().sum::<SnailfishNumber>().magnitude()
}

#[aoc(day18, part2)]
fn largest_magnitude(homework: &Vec<SnailfishNumber>) -> u32 {
    homework
        .iter()
        .permutations(2)
        .map(|pair| (pair[0] + pair[1]).magnitude())
        .max()
        .unwrap_or_default()
}

#[cfg(test)]
mod tests {
    use super::*;

    static EXAMPLE_LINES: [&str; 7] = [
        "[1,2]",
        "[[1,2],3]",
        "[9,[8,7]]",
        "[[1,9],[8,5]]",
        "[[[[1,2],[3,4]],[[5,6],[7,8]]],9]",
        "[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]",
        "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]",
    ];

    static EXAMPLE_MAGNITUDES: [(&str, u32); 6] = [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        (
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
            3488,
        ),
    ];

    static EXAMPLE_SUMS: [(&str, &str); 5] = [
        (
            "[[[[4,3],4],4],[7,[[8,4],9]]]\n[1,1]",
            "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
        ),
        (
            "[1,1]\n[2,2]\n[3,3]\n[4,4]",
            "[[[[1,1],[2,2]],[3,3]],[4,4]]",
        ),
        (
            "[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]",
            "[[[[3,0],[5,3]],[4,4]],[5,5]]",
        ),
        (
            "[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]",
            "[[[[5,0],[7,4]],[5,5]],[6,6]]",
        ),
        (
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]\n\
             [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]\n\
             [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]\n\
             [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]\n\
             [7,[5,[[3,8],[1,4]]]]\n[[2,[2,2]],[8,[8,1]]]\n\
             [2,9]\n[1,[[[9,3],9],[[9,0],[0,7]]]]\n[[[5,[7,4]],7],1]\n\
             [[[[4,2],2],6],[8,7]]",
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
        ),
    ];

    static EXAMPLE_HOMEWORK: &str = "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]\n\
         [[[5,[2,8]],4],[5,[[9,9],0]]]\n\
         [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]\n\
         [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]\n\
         [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]\n\
         [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]\n\
         [[[[5,4],[7,7]],8],[[8,3],8]]\n\
         [[9,3],[[9,9],[6,[4,9]]]]\n\
         [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]\n\
         [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]";

    #[test]
    fn test_parse() -> Result<(), ParseError> {
        for line in EXAMPLE_LINES.iter() {
            let number: SnailfishNumber = line.parse()?;
            assert_eq!(line, &format!("{}", number));
        }
        Ok(())
    }

    #[test]
    fn test_magnitudes() -> Result<(), ParseError> {
        for (line, magnitude) in EXAMPLE_MAGNITUDES.iter() {
            let number: SnailfishNumber = line.parse()?;
            assert_eq!(number.magnitude(), *magnitude);
        }
        Ok(())
    }

    #[test]
    fn test_sums() -> Result<(), ParseError> {
        for (lines, expected) in EXAMPLE_SUMS.iter() {
            let nodes: Vec<SnailfishNumber> = parse_homework(lines)?;
            let res: SnailfishNumber = nodes.iter().sum();
            assert_eq!(&format!("{}", res), expected);
        }
        Ok(())
    }

    #[test]
    fn test_homework_sum() -> Result<(), ParseError> {
        let nodes: Vec<SnailfishNumber> = parse_homework(EXAMPLE_HOMEWORK)?;
        assert_eq!(sum_numbers(&nodes), 4140);
        Ok(())
    }

    #[test]
    fn test_homework_largest_magnitude() -> Result<(), ParseError> {
        let nodes: Vec<SnailfishNumber> = parse_homework(EXAMPLE_HOMEWORK)?;
        assert_eq!(largest_magnitude(&nodes), 3993);
        Ok(())
    }
}
