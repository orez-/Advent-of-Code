use std::env;
use std::io::{self, BufRead};

type Direction = (isize, isize);

struct Sokoban {
    robot: (usize, usize),
    grid: Vec<Vec<Tile>>,
}

fn display(sokoban: &Sokoban) {
    let mut out = String::new();
    for (y, row) in sokoban.grid.iter().enumerate() {
        for (x, elem) in row.iter().enumerate() {
            if (x, y) == sokoban.robot {
                out.push('@');
            } else {
                match elem {
                    Tile::Block => out.push('O'),
                    Tile::Floor => out.push('.'),
                    Tile::Wall => out.push('#'),
                }
            }
        }
        out.push('\n');
    }
    println!("{out}");
}

#[derive(Clone, Copy)]
enum Tile {
    Block,
    Floor,
    Wall,
}

fn part1((mut sokoban, directions): (Sokoban, Vec<Direction>)) -> usize {
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
        display(&sokoban);
    }

    let mut total = 0;
    for (y, row) in sokoban.grid.iter().enumerate() {
        for (x, elem) in row.iter().enumerate() {
            if matches!(elem, Tile::Block) {
                total += y * 100 + x;
            }
        }
    }
    total
}

fn part2((mut sokoban, directions): (Sokoban, Vec<Direction>)) -> u64 {
    todo!();
}

fn read_lines() -> (Sokoban, Vec<Direction>) {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines().map(|line| line.unwrap());
    let mut robot = None;
    let grid = lines.by_ref().take_while(|line| !line.is_empty()).enumerate().map(|(y, row)| {
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
    let sokoban = Sokoban { grid, robot: robot.unwrap() };
    let directions = lines.flat_map(|line| line.into_bytes()).map(|c| match c {
        b'^' => (0, -1),
        b'>' => (1, 0),
        b'v' => (0, 1),
        b'<' => (-1, 0),
        c => panic!("can't do a {c}"),
    }).collect();
    (sokoban, directions)
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
