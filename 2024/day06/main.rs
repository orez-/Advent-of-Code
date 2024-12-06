use std::collections::HashSet;
use std::env;
use std::io::{self, BufRead};

type Grid = Vec<Vec<u8>>;
type Coord = (usize, usize);

fn find_start(grid: &Grid) -> Coord {
    grid.iter().enumerate().find_map(|(y, line)| {
        let x = line.iter().position(|&elem| elem == b'^')?;
        Some((x, y))
    }).unwrap()
}

/// Walk the grid starting at `(x, y)` and apply fn `each` at each position.
/// `each` returns if we should continue walking: if we should stop walking,
/// `walk` returns `true`. `walk` returns `false` instead if we walk out
/// of the grid.
fn walk<F>((mut x, mut y): Coord, grid: &Grid, mut each: F) -> bool
where
    F: FnMut(usize, usize, isize, isize) -> bool,
{
    let width = grid[0].len();
    let height = grid.len();

    let mut dx = 0isize;
    let mut dy = -1isize;

    loop {
        if !each(x, y, dx, dy) {
            return true;
        }
        let nx = x.wrapping_add_signed(dx);
        let ny = y.wrapping_add_signed(dy);
        if nx >= width || ny >= height {
            break;
        }
        if grid[ny][nx] == b'#' {
            (dx, dy) = (-dy, dx);
        } else {
            (x, y) = (nx, ny)
        }
    }
    false
}

fn part1(grid: Grid) -> usize {
    let start = find_start(&grid);

    let mut seen = HashSet::new();
    walk(start, &grid, |x, y, _, _| {
        seen.insert((x, y));
        true
    });
    seen.len()
}

fn part2(mut grid: Grid) -> usize {
    let width = grid[0].len();
    let height = grid.len();
    let start = find_start(&grid);

    let mut seen = HashSet::new();
    let mut total = 0;
    for ox in 0..width {
        for oy in 0..height {
            if grid[oy][ox] != b'.' { continue }
            grid[oy][ox] = b'#';

            seen.clear();
            total += walk(start, &grid, |x, y, dx, dy| seen.insert((x, y, dx, dy))) as usize;

            grid[oy][ox] = b'.';
        }
    }
    total
}

fn read_lines() -> io::Result<Grid> {
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
