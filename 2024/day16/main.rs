use std::collections::{BinaryHeap, HashSet};
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

fn part2(game: Game) -> i32 {
    let _ = game;
    0
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
