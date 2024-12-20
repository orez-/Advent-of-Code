use std::collections::HashMap;
use std::env;
use std::io::{self, BufRead};

type Coord = (usize, usize);
type Grid = Vec<Vec<u8>>;

struct Race {
    grid: Grid,
    start: Coord,
    end: Coord,
}

// "been" is probably more accurately "distance_along_race". whatever.
fn get_been(race: &Race) -> HashMap<Coord, usize> {
    let mut been = HashMap::new();
    let (mut x, mut y) = race.start;
    let mut distance = 0usize;
    loop {
        been.insert((x, y), distance);
        if (x, y) == race.end { break }

        for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0)] {
            let nx = x.wrapping_add_signed(dx);
            let ny = y.wrapping_add_signed(dy);
            // `try_insert` is nightly only as of 1.83
            if race.grid[ny][nx] == b'#' || been.contains_key(&(nx, ny)) { continue };
            (x, y) = (nx, ny);
            distance += 1;
            break;
        }
    }
    been
}

fn part1(race: Race) -> u64 {
    let interesting_cheat_benefit = 100;

    let been = get_been(&race);

    // count good cheats
    let mut count = 0;
    for (&(x, y), d0) in &been {
        if let Some(d1) = been.get(&(x + 2, y)) {
            let cheat_benefit = d0.abs_diff(*d1) - 2;
            if cheat_benefit >= interesting_cheat_benefit {
                count += 1;
            }
        }
        if let Some(d1) = been.get(&(x, y + 2)) {
            let cheat_benefit = d0.abs_diff(*d1) - 2;
            if cheat_benefit >= interesting_cheat_benefit {
                count += 1;
            }
        }
    }
    count
}

fn part2(race: Race) -> u64 {
    let cheat_limit = 20;
    let interesting_cheat_benefit = 100;

    let been = get_been(&race);
    let mut count = 0;

    // bad, jail
    for ((x0, y0), d0) in &been {
        for ((x1, y1), d1) in &been {
            let dist = x0.abs_diff(*x1) + y0.abs_diff(*y1);
            if dist > cheat_limit { continue }
            let cheat_benefit = d0.abs_diff(*d1) - dist;
            if cheat_benefit >= interesting_cheat_benefit {
                count += 1;
            }
        }
    }
    count / 2
}

fn read_lines() -> io::Result<Race> {
    let stdin = io::stdin();
    let grid: io::Result<Vec<Vec<u8>>> = stdin.lock().lines().map(|line| Ok(line?.into_bytes())).collect();
    let mut grid = grid?;
    let find = |grid: &mut Grid, needle: u8| {
        let (x, y) = grid.iter().enumerate()
            .find_map(|(y, row)| row.iter().position(|&elem| elem == needle).map(|x| (x, y)))
            .unwrap();
        grid[y][x] = b'.';
        (x, y)
    };
    let start = find(&mut grid, b'S');
    let end = find(&mut grid, b'E');
    Ok(Race { grid, start, end })
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
