use std::env;
use std::io::{self, BufRead};
use std::collections::{HashMap, HashSet, VecDeque};

type Coord = (usize, usize);
// width and height are _inclusive_!
const WIDTH: usize = 70;
const HEIGHT: usize = 70;

fn find_path(obstacles: &HashMap<Coord, usize>, time: usize) -> Result<i32, ()> {
    let mut been = HashSet::from([(0, 0)]);
    let mut frontier = VecDeque::from([(0, 0, 0)]);
    while let Some((d, x, y)) = frontier.pop_front() {
        if (x, y) == (WIDTH, HEIGHT) { return Ok(d) }
        for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0)] {
            let nx = x.wrapping_add_signed(dx);
            let ny = y.wrapping_add_signed(dy);
            if nx > WIDTH || ny > HEIGHT { continue }
            if obstacles.get(&(nx, ny)).is_some_and(|&t| t < time) { continue }
            if !been.insert((nx, ny)) { continue }
            frontier.push_back((d + 1, nx, ny));
        }
    }
    Err(())
}

fn part1(obstacles: HashMap<Coord, usize>) -> i32 {
    find_path(&obstacles, 1024).expect("oh god we're trapped")
}

fn part2(obstacles: HashMap<Coord, usize>) -> String {
    let mut low = 1024;
    let mut high = obstacles.len() + 1;
    while low < high {
        let mid = (low + high) / 2;
        if find_path(&obstacles, mid).is_ok() {
            low = mid + 1;
        } else {
            high = mid;
        }
    }

    assert!(find_path(&obstacles, low - 1).is_ok(), "too high");
    assert!(find_path(&obstacles, low).is_err(), "too low");

    let ((x, y), _) = obstacles.iter().find(|(_, t)| **t == low - 1).unwrap();
    format!("{x},{y}")
}

fn read_lines() -> io::Result<HashMap<Coord, usize>> {
    let stdin = io::stdin();
    stdin.lock().lines().enumerate().map(|(idx, line)| {
        let line = line?;
        let (x, y) = line.split_once(",").unwrap();
        let x = x.parse().unwrap();
        let y = y.parse().unwrap();
        Ok(((x, y), idx))
    }).collect()
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
