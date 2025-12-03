use std::env;
use std::io::{self, BufRead};
use std::cmp::Reverse;

fn find_batteries(banks: Vec<String>, digits: usize) -> u64 {
    let mut out = 0;
    for bank in banks {
        let bank: Vec<_> = bank.bytes().map(|x| (x - b'0') as u64).collect();
        let mut bank: &[_] = &bank;

        let mut num = 0;
        for remaining in (0..digits).rev() {
            let init = bank.len() - remaining;
            let (idx, digit) = bank[..init]
                .iter()
                .copied()
                .enumerate()
                .max_by_key(|&(i, e)| (e, Reverse(i)))
                .expect("at least one element");
            bank = &bank[idx+1..];
            num *= 10;
            num += digit;
        }
        out += num;
    }
    out
}

fn read_lines() -> io::Result<Vec<String>> {
    let stdin = io::stdin();
    stdin.lock().lines().collect()
}

fn main() -> io::Result<()> {
    match env::args().nth(1).as_deref() {
        Some("part1") => println!("{}", find_batteries(read_lines()?, 2)),
        Some("part2") => println!("{}", find_batteries(read_lines()?, 12)),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
    Ok(())
}
