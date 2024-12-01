use std::collections::HashMap;
use std::env;
use std::io::{self, BufRead};
use std::iter::zip;

fn part1(lines: Vec<String>) -> i32 {
    let mut left: Vec<i32> = Vec::new();
    let mut right: Vec<i32> = Vec::new();

    for line in lines {
        let list: Vec<_> = line.split_ascii_whitespace().collect();
        left.push(list[0].parse().unwrap());
        right.push(list[1].parse().unwrap());
    }

    left.sort();
    right.sort();

    zip(left, right).map(|(a, b)| (a - b).abs()).sum()
}

fn part2(lines: Vec<String>) -> i32 {
    let mut left: Vec<i32> = Vec::new();
    let mut right: HashMap<i32, i32> = HashMap::new();

    for line in lines {
        let list: Vec<_> = line.split_ascii_whitespace().collect();
        left.push(list[0].parse().unwrap());
        *right.entry(list[1].parse().unwrap()).or_default() += 1;
    }

    let mut total = 0;
    for num in left {
        total += num * right.get(&num).unwrap_or(&0);
    }
    total
}

fn read_lines() -> io::Result<Vec<String>> {
    let stdin = io::stdin();
    stdin.lock().lines().collect()
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
