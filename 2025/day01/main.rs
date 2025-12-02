use std::env;
use std::io::{self, BufRead};

fn part1(turns: &[i32]) -> i32 {
    let mut cur = 50;
    let mut count = 0;
    for &turn in turns {
        cur += turn;
        cur = cur.rem_euclid(100);
        if cur == 0 {
            count += 1;
        }
    }
    count
}

fn part2(turns: &[i32]) -> i32 {
    let mut cur = 50;
    let mut count = 0;
    for &turn in turns {
        // weird special case, w/e
        if cur > 0 && cur + turn <= 0 {
            count += 1;
        }
        cur += turn;
        if cur >= 100 {
            count += cur / 100;
        }
        if cur <= 0 {
            count += cur / -100;
        }
        cur = cur.rem_euclid(100);
    }
    count
}

fn read_lines() -> io::Result<Vec<i32>> {
    let stdin = io::stdin();
    stdin
        .lock()
        .lines()
        .map(|line| line.map(|line| line.replace("L", "-").replace("R", "").parse().unwrap()))
        .collect()
}

fn main() -> io::Result<()> {
    match env::args().nth(1).as_deref() {
        Some("part1") => println!("{}", part1(&read_lines()?)),
        Some("part2") => println!("{}", part2(&read_lines()?)),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
    Ok(())
}
