use std::env;
use std::io::{self, BufRead};

fn part1(lines: Vec<String>) -> usize {
    lines
        .iter()
        .filter(|line| {
            let row: Vec<i32> = line
                .split_ascii_whitespace()
                .map(|num| num.parse().unwrap())
                .collect();
            is_safe(&row)
        })
        .count()
}

fn is_safe(row: &[i32]) -> bool {
    let steppy = row.windows(2).all(|v| (v[0] - v[1]).abs() <= 3);
    let sorted = row.windows(2).all(|v| v[0] < v[1]) || row.windows(2).all(|v| v[0] > v[1]);
    steppy && sorted
}

fn part2(lines: Vec<String>) -> usize {
    lines
        .iter()
        .filter(|line| {
            let mut row: Vec<i32> = line
                .split_ascii_whitespace()
                .map(|num| num.parse().unwrap())
                .collect();
            is_safe(&row)
                || (0..row.len()).any(|idx| {
                    let num = row.remove(idx);
                    let safe = is_safe(&row);
                    row.insert(idx, num);
                    safe
                })
        })
        .count()
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
