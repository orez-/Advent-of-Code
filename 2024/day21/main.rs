use std::collections::HashMap;
use std::env;
use std::io::{self, BufRead};
use std::iter::{once, repeat_n};

mod debug;

#[derive(Clone, Copy, PartialEq, Eq)]
enum DirPad {
    Up,
    Right,
    Down,
    Left,
    A,
}

type Coord = (u8, u8);

fn numpad_coord(chr: char) -> Coord {
    match chr {
        '0' => (1, 3),
        '1' => (0, 2),
        '2' => (1, 2),
        '3' => (2, 2),
        '4' => (0, 1),
        '5' => (1, 1),
        '6' => (2, 1),
        '7' => (0, 0),
        '8' => (1, 0),
        '9' => (2, 0),
        'A' => (2, 3),
        _ => panic!(),
    }
}

fn dirpad_coord(dirpad: DirPad) -> Coord {
    match dirpad {
        DirPad::Up => (1, 0),
        DirPad::Right => (2, 1),
        DirPad::Down => (1, 1),
        DirPad::Left => (0, 1),
        DirPad::A => (2, 0),
    }
}

fn paths_to(from: Coord, to: Coord, no_touchie: Coord) -> Vec<Vec<DirPad>> {
    let left = repeat_n(DirPad::Left, from.0.saturating_sub(to.0) as _);
    let right = repeat_n(DirPad::Right, to.0.saturating_sub(from.0) as _);
    let up = repeat_n(DirPad::Up, from.1.saturating_sub(to.1) as _);
    let down = repeat_n(DirPad::Down, to.1.saturating_sub(from.1) as _);
    let press = once(DirPad::A);

    let mut paths = Vec::new();
    // prefer horiz, then vertical
    if !(from.1 == no_touchie.1 && to.0 == no_touchie.0) {
        paths.push(
            left.clone()
                .chain(right.clone())
                .chain(up.clone())
                .chain(down.clone())
                .chain(press.clone())
                .collect()
        );
    }
    // prefer vertical, then horiz
    if !(from.0 == no_touchie.0 && to.1 == no_touchie.1) {
        paths.push(
            up.chain(down).chain(left).chain(right).chain(press).collect()
        );
    }
    paths
}

type Cache = HashMap<(Coord, Coord, usize), usize>;

fn solve_dirpad(cache: &mut Cache, from: Coord, to: Coord, depth: usize) -> usize {
    if depth == 0 { return 1 }

    let key = (from, to, depth);
    if let Some(&ans) = cache.get(&key) { return ans }

    let ans = paths_to(from, to, (0, 0)).into_iter().map(|path| {
        let mut dir_prev = dirpad_coord(DirPad::A);
        let mut score = 0;
        for dir in path {
            let dir_cur = dirpad_coord(dir);
            score += solve_dirpad(cache, dir_prev, dir_cur, depth - 1);
            dir_prev = dir_cur;
        }
        score
    }).min().unwrap();

    cache.insert(key, ans);
    ans
}

fn solve_numpad(cache: &mut Cache, from: Coord, to: Coord, depth: usize) -> usize {
    let key = (from, to, depth + 1);
    if let Some(&ans) = cache.get(&key) { return ans }

    let ans = paths_to(from, to, (0, 3)).into_iter().map(|path| {
        let mut dir_prev = dirpad_coord(DirPad::A);
        let mut score = 0;
        for dir in path {
            let dir_cur = dirpad_coord(dir);
            score += solve_dirpad(cache, dir_prev, dir_cur, depth);
            dir_prev = dir_cur;
        }
        score
    }).min().unwrap();

    cache.insert(key, ans);
    ans
}

fn solve(lines: Vec<String>, depth: usize) -> usize {
    let mut cache = HashMap::new();
    lines.iter().map(|line| {
        let mut score = 0;
        let mut from = numpad_coord('A');
        for chr in line.chars() {
            let to = numpad_coord(chr);
            score += solve_numpad(&mut cache, from, to, depth);
            from = to;
        }
        let num: usize = line[..3].parse().unwrap();
        num * score
    }).sum()
}

fn part1(lines: Vec<String>) -> usize {
    solve(lines, 2)
}

fn part2(lines: Vec<String>) -> usize {
    solve(lines, 25)
}

fn read_lines() -> io::Result<Vec<String>> {
    let stdin = io::stdin();
    stdin.lock().lines().collect()
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
