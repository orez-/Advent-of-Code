use std::env;
use std::io::{self, BufRead};
use std::iter::repeat;

type Grid = Vec<Vec<u8>>;

fn is_xmas(grid: &Grid, coords: impl Iterator<Item=(usize, usize)>) -> bool {
    coords.map(|(y, x)| grid[y][x]).eq(*b"XMAS")
}

fn part1(grid: Grid) -> usize {
    let width = grid[0].len();
    let height = grid.len();
    let mut total = 0;
    for y in 0..height {
        for x in 0..width {
            let up = (y.saturating_sub(3)..=y).rev();
            let down = y..height.min(y+4);
            let left = (x.saturating_sub(3)..=x).rev();
            let right = x..width.min(x+4);

            total += is_xmas(&grid, up.clone().zip(repeat(x))) as usize;
            total += is_xmas(&grid, up.clone().zip(right.clone())) as usize;
            total += is_xmas(&grid, repeat(y).zip(right.clone())) as usize;
            total += is_xmas(&grid, down.clone().zip(right)) as usize;
            total += is_xmas(&grid, down.clone().zip(repeat(x))) as usize;
            total += is_xmas(&grid, down.clone().zip(left.clone())) as usize;
            total += is_xmas(&grid, repeat(y).zip(left.clone())) as usize;
            total += is_xmas(&grid, up.zip(left)) as usize;
        }
    }
    total
}

fn part2(grid: Grid) -> usize {
    let width = grid[0].len();
    let height = grid.len();
    let mut total = 0;
    for y in 0..height {
        for x in 0..width {
            let down = y..height.min(y+3);
            let right = x..width.min(x+3);
            let up = down.clone().rev();
            let left = right.clone().rev();

            let negative =
                down.clone().zip(right.clone()).map(|(y, x)| grid[y][x]).eq(*b"MAS") ||
                up.clone().zip(left.clone()).map(|(y, x)| grid[y][x]).eq(*b"MAS");

            let positive =
                down.zip(left).map(|(y, x)| grid[y][x]).eq(*b"MAS") ||
                up.zip(right).map(|(y, x)| grid[y][x]).eq(*b"MAS");

            total += (positive && negative) as usize;
        }
    }
    total
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
