use std::collections::{HashMap, HashSet};
use std::env;
use std::io::{self, BufRead};

type Grid = Vec<Vec<u8>>;
type Coord = (usize, usize);

fn part1(lines: Grid) -> usize {
    let width = lines[0].len();
    let height = lines.len();
    let mut positions: HashMap<u8, Vec<Coord>> = HashMap::new();
    for (y, line) in lines.iter().enumerate() {
        for (x, &elem) in line.iter().enumerate() {
            if elem == b'.' { continue }
            positions.entry(elem).or_default().push((x, y));
        }
    }

    let mut antinodes: HashSet<Coord> = HashSet::new();
    for coords in positions.values() {
        for (idx, &(x0, y0)) in coords.iter().enumerate() {
            for &(x1, y1) in &coords[..idx] {
                let dx = x1 as isize - x0 as isize;
                let dy = y1 as isize - y0 as isize;
                let ax0 = x0.wrapping_add_signed(-dx);
                let ay0 = y0.wrapping_add_signed(-dy);
                if ax0 < width && ay0 < height {
                    antinodes.insert((ax0, ay0));
                }
                let ax1 = x1.wrapping_add_signed(dx);
                let ay1 = y1.wrapping_add_signed(dy);
                if ax1 < width && ay1 < height {
                    antinodes.insert((ax1, ay1));
                }
            }
        }
    }
    antinodes.len()
}

fn part2(lines: Grid) -> usize {
    let width = lines[0].len();
    let height = lines.len();
    let mut positions: HashMap<u8, Vec<Coord>> = HashMap::new();
    for (y, line) in lines.iter().enumerate() {
        for (x, &elem) in line.iter().enumerate() {
            if elem == b'.' { continue }
            positions.entry(elem).or_default().push((x, y));
        }
    }

    let mut antinodes: HashSet<Coord> = HashSet::new();
    for coords in positions.values() {
        for (idx, &(x0, y0)) in coords.iter().enumerate() {
            for &(x1, y1) in &coords[..idx] {
                let dx = x1 as isize - x0 as isize;
                let dy = y1 as isize - y0 as isize;
                let mut x0 = x0;
                let mut y0 = y0;
                let mut x1 = x1;
                let mut y1 = y1;
                while x0 < width && y0 < height {
                    antinodes.insert((x0, y0));
                    x0 = x0.wrapping_add_signed(-dx);
                    y0 = y0.wrapping_add_signed(-dy);
                }
                while x1 < width && y1 < height {
                    antinodes.insert((x1, y1));
                    x1 = x1.wrapping_add_signed(dx);
                    y1 = y1.wrapping_add_signed(dy);
                }
            }
        }
    }
    antinodes.len()
}

fn read_lines() -> io::Result<Grid> {
    let stdin = io::stdin();
    stdin.lock().lines().map(|line| Ok(line?.into_bytes())).collect()
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
