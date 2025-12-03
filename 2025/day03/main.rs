use std::env;
use std::io::{self, BufRead};
use std::cmp::Reverse;

fn part1(banks: Vec<String>) -> u32 {
    let mut out = 0;
    for bank in banks {
        let mut bank = bank.into_bytes();
        bank.iter_mut().for_each(|x| *x -= b'0');
        let init = bank.len() - 1;
        let (idx, tens) = bank[..init]
            .iter()
            .copied()
            .enumerate()
            .max_by_key(|&(i, e)| (e, Reverse(i)))
            .expect("at least one element");
        let ones = bank[idx+1..].iter().max().expect("at least one element");
        let val = (tens * 10 + ones) as u32;
        out += val;
    }
    out
}

fn part2(banks: Vec<String>) -> u64 {
    let mut out = 0;
    for bank in banks {
        let bank: Vec<_> = bank.bytes().map(|x| (x - b'0') as u64).collect();
        let mut bank: &[_] = &bank;

        let mut num = 0;
        for remaining in (0..12).rev() {
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
        Some("part1") => println!("{}", part1(read_lines()?)),
        Some("part2") => println!("{}", part2(read_lines()?)),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
    Ok(())
}
