use std::collections::{BinaryHeap, HashMap, HashSet};
use std::env;
use std::io::{self, BufRead};

type Grid = Vec<Vec<u8>>;
type Coord = (usize, usize);

struct Game {
    grid: Grid,
    start: Coord,
    end: Coord,
}

fn part1(game: Game) -> i32 {
    let Game {
        grid,
        start: (sx, sy),
        end: (ex, ey),
    } = game;

    let mut been = HashSet::new();
    let mut frontier = BinaryHeap::from([(0, sx, sy, 1, 0)]);
    while let Some((d, x, y, fx, fy)) = frontier.pop() {
        if (x, y) == (ex, ey) { return -d }
        if !been.insert((x, y, fx, fy)) { continue }

        // the 180˚ only matters on the first step but i do not want to special case this.
        for (dx, dy, cost) in [(fx, fy, 1), (-fy, fx, 1001), (fy, -fx, 1001), (-fx, -fy, 2001)] {
            let nx = x.wrapping_add_signed(dx);
            let ny = y.wrapping_add_signed(dy);
            if grid[ny][nx] == b'#' || been.contains(&(nx, ny, dx, dy)) { continue }
            frontier.push((d - cost, nx, ny, dx, dy));
        }
    }
    panic!("oh god we're trapped");
}

fn part2(game: Game) -> usize {
    let Game {
        grid,
        start: (sx, sy),
        end: (ex, ey),
    } = game;

    // distance from start to all relevant cells
    let mut start_to_dist = HashMap::new();
    let mut best = None;
    let mut frontier = BinaryHeap::from([(0, sx, sy, 1, 0)]);
    while let Some((d, x, y, fx, fy)) = frontier.pop() {
        // remaining paths are worse.
        if best.is_some_and(|b| b != d) { break }

        // `try_insert` is nightly-only as of 1.83
        let key = (x, y, fx, fy);
        if start_to_dist.contains_key(&key) { continue }
        start_to_dist.insert(key, d);

        if (x, y) == (ex, ey) {
            best = Some(d);
            continue;
        }

        for (nx, ny, dx, dy, cost) in [
            (x.wrapping_add_signed(fx), y.wrapping_add_signed(fy), fx, fy, 1),
            (x, y, -fy, fx, 1000),
            (x, y, fy, -fx, 1000),
        ] {
            if grid[ny][nx] == b'#' || start_to_dist.contains_key(&(nx, ny, dx, dy)) { continue }
            frontier.push((d - cost, nx, ny, dx, dy));
        }
    }

    // distance from end to all relevant cells
    let mut end_to_dist = HashMap::new();
    let best = best.expect("oh god we're trapped");
    let mut frontier = BinaryHeap::from([
        (0, ex, ey, 1, 0),
        (0, ex, ey, 0, 1),
        (0, ex, ey, -1, 0),
        (0, ex, ey, 0, -1),
    ]);
    while let Some((d, x, y, fx, fy)) = frontier.pop() {
        // remaining paths are worse.
        if best > d { break }

        // `try_insert` is nightly-only as of 1.83
        let key = (x, y, fx, fy);
        if end_to_dist.contains_key(&key) { continue }
        end_to_dist.insert(key, d);

        for (nx, ny, dx, dy, cost) in [
            (x.wrapping_add_signed(fx), y.wrapping_add_signed(fy), fx, fy, 1),
            (x, y, -fy, fx, 1000),
            (x, y, fy, -fx, 1000),
        ] {
            if grid[ny][nx] == b'#' || end_to_dist.contains_key(&(nx, ny, dx, dy)) { continue }
            frontier.push((d - cost, nx, ny, dx, dy));
        }
    }

    let happy_cells: HashSet<_> = end_to_dist.into_iter().filter_map(|((x, y, fx, fy), dist)| {
        let rev_key = (x, y, -fx, -fy);
        let start_dist = start_to_dist.get(&rev_key)?;
        (start_dist + dist == best).then_some((x, y))
    }).collect();
    happy_cells.len()
}

fn read_lines() -> io::Result<Game> {
    let stdin = io::stdin();
    let grid: io::Result<Grid> = stdin.lock().lines().map(|line| Ok(line?.into_bytes())).collect();
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
    Ok(Game { grid, start, end })
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
