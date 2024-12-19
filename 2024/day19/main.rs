use std::collections::{HashSet, VecDeque};
use std::env;
use std::io::{self, BufRead};

struct Input {
    patterns: Trie,
    goals: Vec<String>,
}

fn chr_to_index(chr: char) -> usize {
    match chr {
        'w' => 0,
        'u' => 1,
        'b' => 2,
        'r' => 3,
        'g' => 4,
        _ => panic!("{chr}"),
    }
}

struct Trie {
    frames: Vec<(bool, [usize; 5])>,
}

impl Trie {
    fn new() -> Self {
        Trie { frames: vec![(false, [0; 5])] }
    }

    fn insert(&mut self, pattern: &str) {
        let mut frame_idx = 0;
        for chr in pattern.chars() {
            let len = self.frames.len();
            let next_idx = chr_to_index(chr);
            let next = &mut self.frames[frame_idx].1[next_idx];
            frame_idx = *next;
            if *next == 0 {
                *next = len;
                frame_idx = len;
                self.frames.push((false, [0; 5]));
            }
        }
        self.frames[frame_idx].0 = true;
    }

    fn prefixes_of<'s, 'h>(&'s self, haystack: &'h str) -> impl Iterator<Item = usize> + use<'s, 'h> {
        let mut frame_idx = 0;
        haystack.chars().map(chr_to_index).map_while(move |next_idx| {
            frame_idx = self.frames[frame_idx].1[next_idx];
            (frame_idx != 0).then(|| self.frames[frame_idx].0)
        }).zip(1..).filter(|&(keep, _)| keep).map(|(_, idx)| idx)
    }
}

fn part1(input: Input) -> usize {
    let Input { patterns, goals } = input;

    goals.iter().filter(|&goal| {
        let mut seen = HashSet::new();
        let mut frontier = VecDeque::from([goal.as_str()]);
        while let Some(goal) = frontier.pop_front() {
            if goal.is_empty() { return true }
            for idx in patterns.prefixes_of(goal) {
                let slice = &goal[idx..];
                if seen.insert(slice.len()) {
                    frontier.push_back(slice);
                }
            }
        }
        false
    }).count()
}

fn part2(input: Input) -> usize {
    let Input { patterns, goals } = input;

    goals.iter().map(|goal| {
        let mut seen = vec![0; goal.len() + 1];
        seen[0] = 1;
        for from_idx in 0..goal.len() {
            let count = seen[from_idx];
            if count == 0 { continue }
            for idx in patterns.prefixes_of(&goal[from_idx..]) {
                seen[from_idx..][idx] += count;
            }
        }
        *seen.last().unwrap()
    }).sum()
}

fn read_lines() -> io::Result<Input> {
    let stdin = io::stdin();
    let lines: Result<Vec<_>, _> = stdin.lock().lines().collect();
    let lines = lines?;
    let [pats, _, goals @ ..] = lines.as_slice() else { panic!() };
    let goals = goals.to_vec();

    let mut patterns = Trie::new();
    for pat in pats.split(", ") {
        patterns.insert(pat);
    }

    Ok(Input { patterns, goals })
}

fn main() -> io::Result<()> {
    match env::args().nth(1).as_deref() {
        Some("part1") => println!("{}", part1(read_lines()?)),
        Some("part2") => println!("{}", part2(read_lines()?)),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
    Ok(())
}
