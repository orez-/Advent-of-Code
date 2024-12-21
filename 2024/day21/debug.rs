#![allow(dead_code)]
use crate::{Coord, DirPad, dirpad_coord, numpad_coord};

pub(super) fn replay_commands(s3: &str) {
    let mut numpad = numpad_coord('A');
    let mut dirpad_inner = dirpad_coord(DirPad::A);
    let mut dirpad_outer = dirpad_coord(DirPad::A);

    let mut s0 = String::new();
    let mut s1 = String::new();
    let mut s2 = String::new();

    let mut len0 = 0;
    let mut len1 = 0;
    let mut len2 = 0;

    for dir3 in s3.chars().map(DirPad::from_chr) {
        len0 += 1;
        len1 += 1;
        len2 += 1;
        if step_pad(&mut dirpad_outer, dir3) {
            let dir2 = coord_to_dirpad(dirpad_outer);
            s2.push_str(&format!("{:>len2$}", dir2.to_chr()));
            len2 = 0;

            if step_pad(&mut dirpad_inner, dir2) {
                let dir1 = coord_to_dirpad(dirpad_inner);
                s1.push_str(&format!("{:>len1$}", dir1.to_chr()));
                len1 = 0;

                if step_pad(&mut numpad, dir1) {
                    let chr = coord_to_numpad(numpad);
                    s0.push_str(&format!("{:>len0$}", chr));
                    len0 = 0;
                }
            }
        }
    }
    println!("{s3}\n{s2}\n{s1}\n{s0}");
}

impl DirPad {
    fn to_chr(&self) -> char {
        match self {
            DirPad::Up => '^',
            DirPad::Right => '>',
            DirPad::Down => 'v',
            DirPad::Left => '<',
            DirPad::A => 'A',
        }
    }

    fn from_chr(chr: char) -> DirPad {
        match chr {
            '^' => DirPad::Up,
            '>' => DirPad::Right,
            'v' => DirPad::Down,
            '<' => DirPad::Left,
            'A' => DirPad::A,
            _ => panic!(),
        }
    }
}

pub(super) fn coord_to_numpad(coord: Coord) -> char {
    match coord {
        (1, 3) => '0',
        (0, 2) => '1',
        (1, 2) => '2',
        (2, 2) => '3',
        (0, 1) => '4',
        (1, 1) => '5',
        (2, 1) => '6',
        (0, 0) => '7',
        (1, 0) => '8',
        (2, 0) => '9',
        (2, 3) => 'A',
        _ => panic!(),
    }
}

pub(super) fn coord_to_dirpad(coord: Coord) -> DirPad {
    match coord {
        (1, 0) => DirPad::Up,
        (2, 1) => DirPad::Right,
        (1, 1) => DirPad::Down,
        (0, 1) => DirPad::Left,
        (2, 0) => DirPad::A,
        _ => panic!(),
    }
}

pub(super) fn step_pad(pad: &mut Coord, dir: DirPad) -> bool {
    match dir {
        DirPad::Up => pad.1 = pad.1.wrapping_sub(1),
        DirPad::Right => pad.0 += 1,
        DirPad::Down => pad.1 += 1,
        DirPad::Left => pad.0 = pad.0.wrapping_sub(1),
        DirPad::A => return true,
    }
    false
}
