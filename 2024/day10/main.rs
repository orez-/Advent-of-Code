use std::collections::HashSet;
use std::env;
use std::io::{self, BufRead};

type Grid = Vec<Vec<u8>>;
type Coord = (usize, usize);

fn trailhead_endpoints(grid: &Grid, endpoints: &mut HashSet<Coord>, x: usize, y: usize, next: u8) {
    if x >= grid[0].len() || y >= grid.len() { return }
    if grid[y][x] != next { return }
    if next == 9 {
        endpoints.insert((x, y));
        return
    }
    for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
        let nx = x.wrapping_add_signed(dx);
        let ny = y.wrapping_add_signed(dy);
        trailhead_endpoints(grid, endpoints, nx, ny, next + 1);
    }
}

fn trailhead_rating(grid: &Grid, x: usize, y: usize, next: u8) -> usize {
    if x >= grid[0].len() || y >= grid.len() { return 0 }
    if grid[y][x] != next { return 0 }
    if next == 9 { return 1 }
    let mut total = 0;
    for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
        let nx = x.wrapping_add_signed(dx);
        let ny = y.wrapping_add_signed(dy);
        total += trailhead_rating(grid, nx, ny, next + 1);
    }
    total
}

fn part1(grid: Grid) -> usize {
    let width = grid[0].len();
    let height = grid.len();
    let mut out = 0;
    for y in 0..height {
        for x in 0..width {
            let mut pts = HashSet::new();
            trailhead_endpoints(&grid, &mut pts, x, y, 0);
            out += pts.len();
        }
    }
    out
}

fn part2(grid: Grid) -> usize {
    let width = grid[0].len();
    let height = grid.len();
    let mut out = 0;
    for y in 0..height {
        for x in 0..width {
            out += trailhead_rating(&grid, x, y, 0);
        }
    }
    out
}

fn read_lines() -> io::Result<Grid> {
    let stdin = io::stdin();
    stdin.lock().lines().map(|line| Ok(line?.bytes().map(|b| b - b'0').collect())).collect()
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
