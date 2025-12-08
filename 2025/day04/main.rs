use std::env;
use std::io::{self, BufRead};

type Warehouse = Vec<Vec<u8>>;

fn part1(lines: Warehouse) -> u64 {
    let height = lines.len();
    let width = lines[0].len();

    let mut reachable = 0;
    for (y, line) in lines.iter().enumerate() {
        for (x, &elem) in line.iter().enumerate() {
            if elem == b'.' { continue }
            assert_eq!(elem, b'@');

            let mut around = 0;
            for sy in y.saturating_sub(1)..=(y+1).min(height-1) {
                for sx in x.saturating_sub(1)..=(x+1).min(width-1) {
                    if lines[sy][sx] == b'@' {
                        around += 1;
                    }
                }
            }
            if around < 5 { reachable += 1 }
        }
    }
    reachable
}

fn part2(mut lines: Warehouse) -> u64 {
    let height = lines.len();
    let width = lines[0].len();

    let mut reachable = 0;
    let mut again = true;
    while again {
        again = false;
        for y in 0..height {
            for x in 0..width {
                let elem = lines[y][x];
                if elem == b'.' { continue }
                assert_eq!(elem, b'@');

                let mut around = 0;
                for sy in y.saturating_sub(1)..=(y+1).min(height-1) {
                    for sx in x.saturating_sub(1)..=(x+1).min(width-1) {
                        if lines[sy][sx] == b'@' {
                            around += 1;
                        }
                    }
                }
                if around < 5 {
                    again = true;
                    reachable += 1;
                    lines[y][x] = b'.';
                }
            }
        }
    }
    reachable
}

fn read_lines() -> io::Result<Warehouse> {
    let stdin = io::stdin();
    stdin.lock().lines().map(|x| x.map(|x| x.into_bytes())).collect()
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
