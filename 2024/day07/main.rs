use std::env;
use std::io::{self, BufRead};

fn part1(lines: Vec<String>) -> u64 {
    let mut total = 0;
    for line in lines {
        let (goal, nums) = line.split_once(": ").unwrap();
        let goal: u64 = goal.parse().unwrap();
        let nums: Vec<u64> = nums.split(' ').map(|num| num.parse().unwrap()).collect();
        let perms = 1 << nums.len() - 1;
        for perm in 0..perms {
            let mut idx = 0;
            let result = nums.iter().copied().reduce(|num, agg| {
                let out =
                    if perm & (1 << idx) != 0 { num + agg }
                    else { num * agg };
                idx += 1;
                out
            }).unwrap();
            if goal == result {
                total += goal;
                break;
            }
        }
    }
    total
}

fn could_num(agg: u64, nums: &[u64], ops: &[u8], goal: u64) -> bool {
    let Some((num, nums)) = nums.split_first() else { return agg == goal };
    for op in ops {
        let next = match op {
            0 => agg + num,
            1 => agg * num,
            2 => agg * 10_u64.pow(num.ilog10() + 1) + num,
            _ => panic!(),
        };
        if could_num(next, nums, ops, goal) {
            return true;
        }
    }
    false
}

fn part2(lines: Vec<String>) -> u64 {
    let mut total = 0;
    for line in lines {
        let (goal, nums) = line.split_once(": ").unwrap();
        let goal: u64 = goal.parse().unwrap();
        let nums: Vec<u64> = nums.split(' ').map(|num| num.parse().unwrap()).collect();

        let (&agg, nums) = nums.split_first().unwrap();
        let ops = vec![0, 1, 2];
        if could_num(agg, nums, &ops, goal) {
            total += goal;
        }
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
