use std::collections::{HashMap, HashSet, VecDeque};
use std::env;
use std::io::{self, BufRead};

const PRUNE: u64 = (1 << 24) - 1;

fn evolve(mut secret: u64) -> u64 {
    secret ^= secret << 6;
    secret &= PRUNE;
    secret ^= secret >> 5;
    secret &= PRUNE;
    secret ^= secret << 11;
    secret &= PRUNE;
    secret
}

fn part1(lines: Vec<u64>) -> u64 {
    lines.into_iter().map(|mut x| { (0..2000).for_each(|_| x = evolve(x)); x }).sum()
}

fn part2(lines: Vec<u64>) -> u64 {
    let mut bananas = HashMap::new();
    for mut secret in lines {
        let mut this_seen = HashSet::new();
        let mut seq = VecDeque::new();
        let mut prev_price = secret % 10;
        for _ in 0..2000 {
            secret = evolve(secret);
            let price = secret % 10;
            let diff = price as i64 - prev_price as i64;
            seq.push_back(diff);
            if seq.len() > 4 { seq.pop_front(); }
            if this_seen.insert(seq.clone()) {
                *bananas.entry(seq.clone()).or_default() += price;
            }
            prev_price = price;
        }
    }
    bananas.into_values().max().unwrap()
}

fn read_lines() -> io::Result<Vec<u64>> {
    let stdin = io::stdin();
    stdin.lock().lines().map(|x| Ok(x?.parse().unwrap())).collect()
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
