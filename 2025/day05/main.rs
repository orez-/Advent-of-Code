use std::cmp::Reverse;
use std::env;
use std::io::{self, BufRead};

fn part1(input: Input) -> usize {
    input
        .queries
        .iter()
        .filter(|query| {
            input.fresh_ranges.iter().any(|(start, end)| (start..=end).contains(query))
        })
        .count()
}

fn part2(input: Input) -> u64 {
    input
        .fresh_ranges
        .iter()
        .fold(0, |agg, (start, end)| agg + end - start + 1)
}

struct Input {
    fresh_ranges: Vec<(u64, u64)>,
    queries: Vec<u64>,
}

fn read_input() -> Input {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines().map(|line| line.expect("io err"));
    let mut ranges: Vec<(u64, u64)> = lines
        .by_ref()
        .take_while(|line| !line.is_empty())
        .map(|line| {
            let (start, end) = line.split_once("-").expect("range contains `-`");
            let start = start.parse().expect("range start is integer");
            let end = end.parse().expect("range end is integer");
            (start, end)
        })
        .collect();
    ranges.sort_by_key(|&(start, end)| (start, Reverse(end)));

    let mut fresh_ranges = Vec::new();
    let (mut range_start, mut range_end) = ranges[0];
    for (start, end) in ranges {
        if (range_start..=range_end).contains(&start) {
            range_end = range_end.max(end);
        } else {
            fresh_ranges.push((range_start, range_end));
            range_start = start;
            range_end = end;
        }
    }
    fresh_ranges.push((range_start, range_end));

    let queries = lines
        .map(|line| line.parse().expect("query is integer"))
        .collect();
    Input { fresh_ranges, queries }
}

fn main() {
    match env::args().nth(1).as_deref() {
        Some("part1") => println!("{}", part1(read_input())),
        Some("part2") => println!("{}", part2(read_input())),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
}
