use std::env;
use std::io::{self, BufRead};

fn part1(sec: Input) -> u64 {
    let mut count = 0;
    for &lock in &sec.locks {
        for &key in &sec.keys {
            if std::iter::zip(lock, key).all(|(a, b)| a <= b) {
                count += 1;
            }
        }
    }
    count
}

fn part2(_: Input) -> &'static str {
    "happy holiday"
}


struct Input {
    locks: Vec<Security>,
    keys: Vec<Security>,
}

type Security = [u8; 5];

fn read_lines() -> Input {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines().map(|x| x.unwrap()); // a xmas miracle!!
    let mut locks = Vec::new();
    let mut keys = Vec::new();
    loop {
        let grid: Vec<_> = lines
            .by_ref()
            .take_while(|line| !line.is_empty())
            .map(|line| line.into_bytes())
            .collect();
        if grid.is_empty() { break }
        let is_lock = grid[0] == b"#####";
        if is_lock {
            let pins: Vec<_> = (0..5).map(|x| (0..7).take_while(|&y| grid[y][x] == b'#').count() as u8).collect();
            let pins = pins.try_into().unwrap();
            locks.push(pins);
        } else {
            let pins: Vec<_> = (0..5).map(|x| (0..7).take_while(|&y| grid[y][x] == b'.').count() as u8).collect();
            let pins = pins.try_into().unwrap();
            keys.push(pins);
        }
    }
    Input { locks, keys }
}

fn main() -> io::Result<()> {
    match env::args().nth(1).as_deref() {
        Some("part1") => println!("{}", part1(read_lines())),
        Some("part2") => println!("{}", part2(read_lines())),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
    Ok(())
}
