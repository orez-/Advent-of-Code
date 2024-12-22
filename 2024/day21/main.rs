use std::collections::{HashSet, VecDeque};
use std::env;
use std::io::{self, BufRead};
use std::iter::{once, repeat_n};
use crate::debug::*;

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

fn move_to(pos: &mut Coord, to: Coord) -> Vec<DirPad> {
    let from = *pos;
    *pos = to;

    let left = repeat_n(DirPad::Left, from.0.saturating_sub(to.0) as _);
    let right = repeat_n(DirPad::Right, to.0.saturating_sub(from.0) as _);
    let up = repeat_n(DirPad::Up, from.1.saturating_sub(to.1) as _);
    let down = repeat_n(DirPad::Down, to.1.saturating_sub(from.1) as _);
    let press = once(DirPad::A);

    if from.0 == 0 {
        // prefer horiz, then vertical
        left.chain(right).chain(up).chain(down).chain(press).collect()
    } else {
        // prefer vertical, then horiz
        up.chain(down).chain(left).chain(right).chain(press).collect()
    }
}

#[derive(Clone, PartialEq, Eq, Hash, Debug)]
struct State<'g, const N: usize> {
    goal: &'g str,
    numpad0: Coord,
    dirpads: [Coord; N],
}

fn in_dirbounds((x, y): Coord) -> bool {
    !(x > 2 || y > 1 || (x, y) == (0, 0))
}

fn in_numbounds((x, y): Coord) -> bool {
    !(x > 2 || y > 3 || (x, y) == (0, 3))
}

fn run<const N: usize>(lines: Vec<String>) -> usize {
    lines.iter().map(|line| {
        let mut score = 0;
        let init = State {
            goal: line,
            dirpads: [dirpad_coord(DirPad::A); N],
            numpad0: numpad_coord('A'),
        };
        let mut seen = HashSet::from([init.clone()]);
        let mut frontier = VecDeque::from([(0, init)]);
        while let Some((steps, state)) = frontier.pop_front() {
            if state.goal.is_empty() {
                score = steps;
                break;
            }
            for mut dir in [DirPad::Up, DirPad::Right, DirPad::Down, DirPad::Left, DirPad::A] {
                let mut state = state.clone();
                'once: loop {
                    'press: loop {
                        for dirpad in &mut state.dirpads {
                            let press = step_pad(dirpad, dir);
                            if !in_dirbounds(*dirpad) { break 'once }
                            if !press { break 'press }
                            dir = coord_to_dirpad(*dirpad);
                        }
                        let press = step_pad(&mut state.numpad0, dir);
                        if !in_numbounds(state.numpad0) { break 'once }
                        if !press { break 'press }

                        // numpad press
                        let mut chrs = state.goal.chars();
                        let exp = chrs.next().unwrap();
                        state.goal = chrs.as_str();
                        if coord_to_numpad(state.numpad0) != exp { break 'once }
                        break;
                    }

                    // progress
                    if seen.insert(state.clone()) {
                        frontier.push_back((steps + 1, state));
                    }
                    break;
                }
            }
        }

        let num: usize = line[..3].parse().unwrap();
        num * score
    }).sum()
}

fn part1(lines: Vec<String>) -> usize {
    run::<2>(lines)
}

fn part2(lines: Vec<String>) -> usize {
    run::<25>(lines)
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
