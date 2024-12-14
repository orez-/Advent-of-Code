use regex::Regex;
use std::env;
use std::io::{self, BufRead};
use std::cmp::Ordering;

const WIDTH: i64 = 101;
const HEIGHT: i64 = 103;

type Vector = (i64, i64);
#[derive(Debug, Clone, PartialEq, Eq)]
struct Robot {
    position: Vector,
    velocity: Vector,
}

fn part1(mut bots: Vec<Robot>) -> u64 {
    step_bots(&mut bots, 100);

    let mut buckets = [0, 0, 0, 0];
    for bot in bots {
        let x = match bot.position.0.cmp(&(WIDTH / 2)) {
            Ordering::Equal => continue,
            Ordering::Less => 0,
            Ordering::Greater => 1,
        };
        let y = match bot.position.1.cmp(&(HEIGHT / 2)) {
            Ordering::Equal => continue,
            Ordering::Less => 0,
            Ordering::Greater => 2,
        };
        buckets[x | y] += 1;
    }
    buckets.into_iter().fold(1, |agg, num| agg * num)
}

fn part2(mut bots: Vec<Robot>) -> u64 {
    step_bots(&mut bots, 28);
    for idx in 0.. {
        display_bots(&bots);
        println!("{}\n", idx * 101 + 28);
        step_bots(&mut bots, 101);
    }
    0
}

fn step_bots(bots: &mut [Robot], steps: i64) {
    for bot in bots {
        bot.position.0 = (bot.position.0 + bot.velocity.0 * steps).rem_euclid(WIDTH);
        bot.position.1 = (bot.position.1 + bot.velocity.1 * steps).rem_euclid(HEIGHT);
    }
}

fn display_bots(bots: &[Robot]) {
    let mut out = String::new();
    for y in 0..HEIGHT {
        for x in 0..WIDTH {
            let count = bots.iter().filter(|bot| bot.position == (x, y)).count();
            if count == 0 {
                out.push('.');
            } else {
                out.push_str(&count.to_string());
            }
        }
        out.push('\n');
    }
    println!("{out}");
}

fn read_lines() -> io::Result<Vec<Robot>> {
    let stdin = io::stdin();
    let re = Regex::new(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)").unwrap();
    stdin.lock().lines().map(|line| {
        let [px, py, vx, vy] = re.captures(&line?).unwrap().extract().1.map(|num| num.parse().unwrap());
        Ok(Robot { position: (px, py), velocity: (vx, vy) })
    }).collect()
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
