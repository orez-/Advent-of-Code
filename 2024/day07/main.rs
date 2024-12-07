use std::env;
use std::io::{self, BufRead};

type Equation = (u64, Vec<u64>);

fn part1_bits(lines: Vec<Equation>) -> u64 {
    let mut total = 0;
    for (goal, nums) in lines {
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

#[derive(Clone, Copy)]
enum Operator {
    Add,
    Multiply,
    Concatenate,
}

fn could_num(agg: u64, nums: &[u64], ops: &[Operator], goal: u64) -> bool {
    let Some((num, nums)) = nums.split_first() else { return agg == goal };
    ops.iter().any(|op| {
        let next = match op {
            Operator::Add => agg + num,
            Operator::Multiply => agg * num,
            Operator::Concatenate => agg * 10_u64.pow(num.ilog10() + 1) + num,
        };
        could_num(next, nums, ops, goal)
    })
}

fn part1(lines: Vec<Equation>) -> u64 {
    let mut total = 0;
    for (goal, nums) in lines {
        let (&agg, nums) = nums.split_first().unwrap();
        let ops = vec![Operator::Add, Operator::Multiply];
        if could_num(agg, nums, &ops, goal) {
            total += goal;
        }
    }
    total
}

fn part2(lines: Vec<Equation>) -> u64 {
    let mut total = 0;
    for (goal, nums) in lines {
        let (&agg, nums) = nums.split_first().unwrap();
        let ops = vec![Operator::Add, Operator::Multiply, Operator::Concatenate];
        if could_num(agg, nums, &ops, goal) {
            total += goal;
        }
    }
    total
}

fn read_lines() -> io::Result<Vec<Equation>> {
    let stdin = io::stdin();
    stdin.lock().lines().map(|line| {
        let line = line?;
        let (goal, nums) = line.split_once(": ").unwrap();
        let goal: u64 = goal.parse().unwrap();
        let nums: Vec<u64> = nums.split(' ').map(|num| num.parse().unwrap()).collect();
        Ok((goal, nums))
    }).collect()
}

fn main() -> io::Result<()> {
    match env::args().nth(1).as_deref() {
        Some("part1_bits") => println!("{}", part1_bits(read_lines()?)),
        Some("part1") => println!("{}", part1(read_lines()?)),
        Some("part2") => println!("{}", part2(read_lines()?)),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
    Ok(())
}
