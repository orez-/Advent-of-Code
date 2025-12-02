use std::env;
use std::io::{self, BufRead};

type Range = (String, String);

fn part1(ranges: Vec<Range>) -> u64 {
    let mut total = 0;
    for (mut start, end) in ranges {
        let s_num: u64 = start.parse().unwrap();
        let e_num: u64 = end.parse().unwrap();
        if start.len() == 1 {
            start = "10".to_string();
        }
        let start_half: u64 = start[..start.len() / 2].parse().unwrap();
        let end_half: u64 = end[..end.len().div_ceil(2)].parse().unwrap();
        for num in start_half..=end_half {
            let num_str = num.to_string().repeat(2);
            let num = num_str.parse().unwrap();
            if (s_num..=e_num).contains(&num) {
                total += num;
            }
        }
    }
    total
}

// PRECONDITION: `start` and `end` have the same number of digits
fn sum_repeats(start: String, end: String) -> u64 {
    // AW. there's gotta be a better (mathy) way to dedupe,
    // but I'm not seeing it right now.
    let mut seen = std::collections::HashSet::new();

    let digits = start.len();
    assert!(digits == end.len(), "{start} and {end} should have same number of digits");

    let mut total = 0;
    let s_num: u64 = start.parse().unwrap();
    let e_num: u64 = end.parse().unwrap();
    let top = end.len().div_ceil(2);
    for len in 1..=top {
        let start_half: u64 = start[..len].parse().unwrap();
        let end_half: u64 = end[..len].parse().unwrap();
        let into = start.len() / len;
        for num in start_half..=end_half {
            let num_str = num.to_string().repeat(into);
            let num = num_str.parse().unwrap();
            if seen.insert(num) && (s_num..=e_num).contains(&num) {
                total += num;
            }
        }
    }
    total
}

fn part2(ranges: Vec<Range>) -> u64 {
    let mut total = 0;
    for (mut start, end) in ranges {
        if start.len() == 1 {
            start = "10".to_string();
        }
        // err wait, this only works when `start` and `end` differ by no more
        // than one. This is the case for my input, but not necessarily in general!
        // ...Oops!
        if start.len() < end.len() {
            let seam = 10_u64.pow(start.len() as _);
            total += sum_repeats(start, (seam-1).to_string());
            total += sum_repeats(seam.to_string(), end);
        } else {
            total += sum_repeats(start, end);
        }
    }
    total
}

fn read_input() -> io::Result<Vec<Range>> {
    let stdin = io::stdin();
    let line = stdin.lock().lines().next().unwrap()?;
    let out = line.split(',').map(|range| {
        let (a, b) = range.split_once('-').unwrap();
        (a.to_string(), b.to_string())
    }).collect();
    Ok(out)
}

fn main() -> io::Result<()> {
    match env::args().nth(1).as_deref() {
        Some("part1") => println!("{}", part1(read_input()?)),
        Some("part2") => println!("{}", part2(read_input()?)),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
    Ok(())
}
