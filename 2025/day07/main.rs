use std::env;
use std::io::{self, BufRead};
use std::collections::HashMap;

fn part1(lines: Vec<String>) -> u64 {
    let start = lines[0].chars().position(|c| c == 'S').expect("start");
    let mut tachyons = vec![start]; // tak-tak-tak
    let mut splits = 0;
    for line in &lines[1..] {
        let line = line.as_bytes();
        let mut new_tachyons = Vec::new();
        for tach in tachyons {
            match line[tach] {
                b'^' => {
                    splits += 1;
                    new_tachyons.extend([tach-1, tach+1]);
                }
                b'.' => {
                    new_tachyons.push(tach);
                }
                b => panic!("unexpected chr {}", b as char),
            }
        }

        new_tachyons.dedup();
        tachyons = new_tachyons;
    }
    splits
}

fn part2(lines: Vec<String>) -> u64 {
    let start = lines[0].chars().position(|c| c == 'S').expect("start");
    let mut tachyons = HashMap::from([(start, 1)]); // ee-on.
    for line in &lines[1..] {
        let line = line.as_bytes();
        let mut new_tachyons = HashMap::new();
        for (tach, count) in tachyons {
            match line[tach] {
                b'^' => {
                    *new_tachyons.entry(tach-1).or_default() += count;
                    *new_tachyons.entry(tach+1).or_default() += count;
                }
                b'.' => {
                    *new_tachyons.entry(tach).or_default() += count;
                }
                b => panic!("unexpected chr {}", b as char),
            }
        }
        tachyons = new_tachyons;
    }
    tachyons.values().sum()
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
