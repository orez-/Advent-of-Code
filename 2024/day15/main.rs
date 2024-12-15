use std::env;
use std::io::{self, BufRead};

type Direction = (isize, isize);

#[derive(Clone)]
struct Sokoban<T> {
    robot: (usize, usize),
    grid: Vec<Vec<T>>,
}

impl<T: Eq> Sokoban<T> {
    fn count_score(&self, tile: &T) -> usize {
        let mut total = 0;
        for (y, row) in self.grid.iter().enumerate() {
            for (x, elem) in row.iter().enumerate() {
                if elem == tile {
                    total += y * 100 + x;
                }
            }
        }
        total
    }
}

impl Sokoban<Tile2> {
    fn shove(&mut self, (x, y): (usize, usize), dir: Direction) -> bool {
        match self.grid[y][x] {
            Tile2::Floor => true,
            Tile2::Wall => false,
            Tile2::BlockLeft => {
                self.grid[y][x] = Tile2::Floor;
                self.grid[y][x + 1] = Tile2::Floor;
                let nx = x.wrapping_add_signed(dir.0);
                let ny = y.wrapping_add_signed(dir.1);
                let can =
                    self.shove((nx, ny), dir) &&
                    self.shove((nx + 1, ny), dir);
                self.grid[ny][nx] = Tile2::BlockLeft;
                self.grid[ny][nx + 1] = Tile2::BlockRight;
                can
            }
            // lazy
            Tile2::BlockRight => self.shove((x - 1, y), dir),
        }
    }
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum Tile {
    Block,
    Floor,
    Wall,
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum Tile2 {
    BlockLeft,
    BlockRight,
    Floor,
    Wall,
}

fn part1((grid, directions): (Vec<String>, Vec<Direction>)) -> usize {
    let mut robot = None;
    let grid = grid.iter().enumerate().map(|(y, row)| {
        row.chars().enumerate().map(|(x, elem)| match elem {
            '@' => {
                robot = Some((x, y));
                Tile::Floor
            }
            '.' => Tile::Floor,
            '#' => Tile::Wall,
            'O' => Tile::Block,
            c => panic!("dunno what a '{c}' is"),
        }).collect()
    }).collect();
    let mut sokoban = Sokoban { grid, robot: robot.unwrap() };

    for (dx, dy) in directions {
        let (x, y) = sokoban.robot;
        let rx = x.wrapping_add_signed(dx);
        let ry = y.wrapping_add_signed(dy);
        let mut nx = rx;
        let mut ny = ry;
        while matches!(sokoban.grid[ny][nx], Tile::Block) {
            nx = nx.wrapping_add_signed(dx);
            ny = ny.wrapping_add_signed(dy);
        }
        match sokoban.grid[ny][nx] {
            Tile::Block => panic!(),
            Tile::Wall => continue,
            Tile::Floor => (),
        }
        let lift = sokoban.grid[ry][rx];
        sokoban.grid[ny][nx] = lift;
        sokoban.grid[ry][rx] = Tile::Floor;
        sokoban.robot = (rx, ry);
    }

    sokoban.count_score(&Tile::Block)
}

fn part2((grid, directions): (Vec<String>, Vec<Direction>)) -> usize {
    let mut robot = None;
    let grid = grid.iter().enumerate().map(|(y, row)| {
        row.chars().enumerate().flat_map(|(x, elem)| match elem {
            '@' => {
                robot = Some((x * 2, y));
                [Tile2::Floor, Tile2::Floor]
            }
            '.' => [Tile2::Floor, Tile2::Floor],
            '#' => [Tile2::Wall, Tile2::Wall],
            'O' => [Tile2::BlockLeft, Tile2::BlockRight],
            c => panic!("dunno what a '{c}' is"),
        }).collect()
    }).collect();
    let mut sokoban = Sokoban { grid, robot: robot.unwrap() };

    for (dx, dy) in directions {
        let mut potential = sokoban.clone();
        let (x, y) = sokoban.robot;
        let rx = x.wrapping_add_signed(dx);
        let ry = y.wrapping_add_signed(dy);
        if potential.shove((rx, ry), (dx, dy)) {
            sokoban = potential;
            sokoban.robot = (rx, ry);
        }
    }

    sokoban.count_score(&Tile2::BlockLeft)
}

fn read_lines() -> (Vec<String>, Vec<Direction>) {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines().map(|line| line.unwrap());
    let grid = lines.by_ref().take_while(|line| !line.is_empty()).collect();

    let directions = lines.flat_map(|line| line.into_bytes()).map(|c| match c {
        b'^' => (0, -1),
        b'>' => (1, 0),
        b'v' => (0, 1),
        b'<' => (-1, 0),
        c => panic!("can't do a {c}"),
    }).collect();
    (grid, directions)
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
