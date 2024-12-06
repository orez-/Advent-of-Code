use std::collections::HashSet;
use std::env;
use std::io::{self, BufRead};

fn part1(lines: Vec<Vec<u8>>) -> usize {
    let width = lines[0].len();
    let height = lines.len();
    let (mut x, mut y) = lines.iter().enumerate().find_map(|(y, line)| {
        let x = line.iter().position(|&elem| elem == b'^')?;
        Some((x, y))
    }).unwrap();
    let mut seen = HashSet::new();
    let mut dx = 0isize;
    let mut dy = -1isize;

    loop {
        seen.insert((x, y));
        let nx = x.wrapping_add_signed(dx);
        let ny = y.wrapping_add_signed(dy);
        if nx >= width || ny >= height { break }
        if lines[ny][nx] == b'#' {
            (dx, dy) = (-dy, dx);
        } else {
            (x, y) = (nx, ny)
        }
    }
    seen.len()
}

fn part2(mut lines: Vec<Vec<u8>>) -> i32 {
    let width = lines[0].len();
    let height = lines.len();
    let (sx, sy) = lines.iter().enumerate().find_map(|(y, line)| {
        let x = line.iter().position(|&elem| elem == b'^')?;
        Some((x, y))
    }).unwrap();

    let mut total = 0;
    for ox in 0..width {
        for oy in 0..height {
            if lines[oy][ox] != b'.' { continue }
            lines[oy][ox] = b'#';

            let mut seen = HashSet::new();
            let mut x = sx;
            let mut y = sy;
            let mut dx = 0isize;
            let mut dy = -1isize;

            loop {
                if !seen.insert((x, y, dx, dy)) {
                    total += 1;
                    break
                }
                let nx = x.wrapping_add_signed(dx);
                let ny = y.wrapping_add_signed(dy);
                if nx >= width || ny >= height {
                    break;
                }
                if lines[ny][nx] == b'#' {
                    (dx, dy) = (-dy, dx);
                } else {
                    (x, y) = (nx, ny)
                }
            };

            lines[oy][ox] = b'.';
        }
    }
    total
}

fn read_lines() -> io::Result<Vec<Vec<u8>>> {
    let stdin = io::stdin();
    stdin.lock().lines().map(|x| Ok(x?.into_bytes())).collect()
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
