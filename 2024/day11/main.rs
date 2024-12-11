use std::collections::HashMap;
use std::env;
use std::io::{self, BufRead};

fn blink(stones: &mut Vec<u64>) {
    *stones = stones.iter().flat_map(|&stone| {
        if stone == 0 {
            return vec![1]
        }
        let digits = stone.ilog10() + 1;
        if digits % 2 == 0 {
            let split = 10_u64.pow(digits / 2);
            let left = stone / split;
            let right = stone % split;
            return vec![left, right]
        }
        vec![stone * 2024]
    }).collect();
}

fn blink2(stones: &mut HashMap<u64, usize>) {
    let mut out = HashMap::new();
    for (&stone, &count) in &*stones {
        if stone == 0 {
            *out.entry(1).or_default() += count;
            continue;
        }
        let digits = stone.ilog10() + 1;
        if digits % 2 == 0 {
            let split = 10_u64.pow(digits / 2);
            let left = stone / split;
            let right = stone % split;
            *out.entry(left).or_default() += count;
            *out.entry(right).or_default() += count;
            continue;
        }
        *out.entry(stone * 2024).or_default() += count;
    }
    *stones = out;
}

fn part1(mut stones: Vec<u64>) -> usize {
    for _ in 0..25 {
        blink(&mut stones);
    }
    stones.len()
}

fn part2(stone_list: Vec<u64>) -> usize {
    let mut stones = HashMap::new();
    for stone in stone_list {
        *stones.entry(stone).or_default() += 1;
    }
    for _ in 0..75 {
        blink2(&mut stones);
    }
    stones.into_values().sum()
}

fn read_line() -> io::Result<Vec<u64>> {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().collect::<io::Result<Vec<_>>>()?;
    let [line] = lines.try_into().unwrap();
    Ok(line.split(" ").map(|x| x.parse().unwrap()).collect())
}

fn main() -> io::Result<()> {
    match env::args().nth(1).as_deref() {
        Some("part1") => println!("{}", part1(read_line()?)),
        Some("part2") => println!("{}", part2(read_line()?)),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
    Ok(())
}
