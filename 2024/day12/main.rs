use std::collections::{BTreeSet, HashSet};
use std::env;
use std::io::{self, BufRead};

type Grid = Vec<Vec<u8>>;

fn part1(grid: Grid) -> usize {
    let width = grid[0].len();
    let height = grid.len();
    let mut seen = HashSet::new();
    let mut fence_cost = 0;
    for sy in 0..height {
        for sx in 0..width {
            if !seen.insert((sx, sy)) { continue }

            let crop = grid[sy][sx];
            let mut region = HashSet::new();
            let mut edges = HashSet::new();
            let mut frontier = vec![(sx, sy)];
            while let Some((x, y)) = frontier.pop() {
                region.insert((x, y));
                let new_edges = [(x, y, true), (x, y, false), (x + 1, y, true), (x, y + 1, false)].into_iter().collect();
                edges = &edges ^ &new_edges;

                for (dx, dy) in [(0, 1), (1, 0), (-1, 0), (0, -1)] {
                    let nx = x.wrapping_add_signed(dx);
                    let ny = y.wrapping_add_signed(dy);
                    if nx >= width || ny >= height || grid[ny][nx] != crop || !seen.insert((nx, ny)) { continue }
                    frontier.push((nx, ny));
                }
            }
            fence_cost += region.len() * edges.len();
        }
    }
    fence_cost
}

#[derive(PartialOrd, Ord, PartialEq, Eq, Clone, Copy, Debug)]
struct Edge {
    x: usize,
    y: usize,
    dir: Direction,
}

impl Edge {
    fn new(x: usize, y: usize, dir: Direction) -> Self {
        Edge { x, y, dir }
    }

    fn rev(&self) -> Edge {
        match self.dir {
            Direction::Up => Edge::new(self.x, self.y - 1, Direction::Down),
            Direction::Down => Edge::new(self.x, self.y + 1, Direction::Up),
            Direction::Left => Edge::new(self.x - 1, self.y, Direction::Right),
            Direction::Right => Edge::new(self.x + 1, self.y, Direction::Left),
        }
    }
}

#[derive(PartialOrd, Ord, PartialEq, Eq, Clone, Copy, Debug)]
enum Direction {
    Left,
    Right,
    Up,
    Down,
}


fn part2(grid: Grid) -> usize {
    let width = grid[0].len();
    let height = grid.len();
    let mut seen = BTreeSet::new();
    let mut fence_cost = 0;
    for sy in 0..height {
        for sx in 0..width {
            if !seen.insert((sx, sy)) { continue }
            let crop = grid[sy][sx];
            let mut region = HashSet::new();
            let mut edges = BTreeSet::new();
            let mut frontier = vec![(sx, sy)];
            while let Some((x, y)) = frontier.pop() {
                region.insert((x, y));

                let new_edges = [
                    Edge::new(x, y, Direction::Right),
                    Edge::new(x + 1, y, Direction::Down),
                    Edge::new(x + 1, y + 1, Direction::Left),
                    Edge::new(x, y + 1, Direction::Up),
                ];
                for edge in new_edges {
                    if !edges.remove(&edge.rev()) {
                        edges.insert(edge);
                    }
                }

                for (dx, dy) in [(0, 1), (1, 0), (-1, 0), (0, -1)] {
                    let nx = x.wrapping_add_signed(dx);
                    let ny = y.wrapping_add_signed(dy);
                    if nx >= width || ny >= height || grid[ny][nx] != crop || !seen.insert((nx, ny)) { continue }
                    frontier.push((nx, ny));
                }
            }

            // count full edges.
            // relies on BTreeSet ordering
            let mut edge_count = 0;
            while let Some(&edge) = edges.first() {
                let mut edge = edge;
                while edges.remove(&edge) {
                    match edge.dir {
                        Direction::Up | Direction::Down => edge.y += 1,
                        Direction::Left | Direction::Right => edge.x += 1,
                    }
                }
                edge_count += 1;
            }

            fence_cost += region.len() * edge_count;
        }
    }
    fence_cost
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
