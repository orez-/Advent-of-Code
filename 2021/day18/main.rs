use std::env;
use std::fmt;
use std::io::{self, BufRead};
use std::mem;

#[derive(Debug)]
enum SnailNumBuilder {
    Empty,
    Number(u32),
    Pair(Box<SnailNumBuilder>, Box<SnailNumBuilder>),
}

impl SnailNumBuilder {
    fn empty_pair() -> Self {
        SnailNumBuilder::Pair(
            Box::new(SnailNumBuilder::Empty),
            Box::new(SnailNumBuilder::Empty),
        )
    }

    fn push_node(&mut self, s: SnailNumBuilder) {
        use SnailNumBuilder::*;
        match self {
            Empty => { *self = s },
            Number(_) => { panic!("Could not push into number"); }
            // wishing for box_patterns
            // https://github.com/rust-lang/rust/issues/29641
            Pair(a, b) => {
                match (&**a, &**b) {
                    (Empty, _) => { **a = s; }
                    (_, Empty) => { **b = s; }
                    _ => { panic!("Could not push into full pair"); }
                }
            }
        }
    }

    fn build(self) -> SnailNum {
        use SnailNumBuilder::*;
        match self {
            Empty => { panic!("incomplete snail num"); }
            Number(n) => SnailNum::Number(n),
            Pair(a, b) => SnailNum::pair(a.build(), b.build()),
        }
    }
}

#[derive(Clone)]
enum SnailNum {
    Number(u32),
    Pair(Box<SnailNum>, Box<SnailNum>),
}

impl SnailNum {
    fn pair(a: SnailNum, b: SnailNum) -> SnailNum {
        SnailNum::Pair(
            Box::new(a),
            Box::new(b),
        )
    }

    fn add(a: SnailNum, b: SnailNum) -> SnailNum {
        let mut num = Self::pair(a, b);
        while num.explode() || num.split() {}
        num
    }

    fn from_line<S: AsRef<str>>(s: S) -> SnailNum {
        use SnailNumBuilder::*;
        let mut stack = Vec::new();

        for chr in s.as_ref().chars() {
            match chr {
                '[' => stack.push(SnailNumBuilder::empty_pair()),
                '0'..='9' => {
                    let num = chr.to_digit(10).unwrap();
                    let node = Number(num);
                    stack.last_mut().unwrap().push_node(node);
                }
                ']' => {
                    let top = stack.pop().unwrap();
                    match stack.last_mut() {
                        Some(new_top) => new_top.push_node(top),
                        None => { return top.build(); }
                    }
                }
                ',' => (),
                _ => panic!("Unexpected character {:?}", chr),
            }
        }
        panic!("unterminated pair");
    }

    fn unwrap_number(self) -> u32 {
        if let SnailNum::Number(num) = self {
            return num;
        }
        panic!("expected Number, got {:?}", self);
    }

    fn unwrap_pair(self) -> (Box<SnailNum>, Box<SnailNum>) {
        if let SnailNum::Pair(left, right) = self {
            return (left, right);
        }
        panic!("expected Pair, got {:?}", self);
    }

    fn explode(&mut self) -> bool {
        self.explode_depth(0).is_some()
    }

    // Return type here is weird:
    // - `None` means we did not find a pair to explode.
    // - `Some((left, right))` means we DID find a pair, and as we
    //     make our way back through the call stack we need to
    //     propagate its `left` and `right`.
    // As soon as we were the right of a pair we can issue
    // an `explode_left` on the left of the pair and `None`-out `left`,
    // and repeat the process with all the directions flipped for `right`.
    fn explode_depth(&mut self, depth: u8) -> Option<(Option<u32>, Option<u32>)> {
        use SnailNum::*;
        match self {
            Number(_) => None,
            Pair(left, right) => {
                if depth >= 4 {
                    let (left, right) = mem::replace(self, Number(0)).unwrap_pair();
                    let num_left = left.unwrap_number();
                    let num_right = right.unwrap_number();
                    return Some((Some(num_left), Some(num_right)));
                }
                if let Some((lsplode, rsplode)) = left.explode_depth(depth + 1) {
                    if let Some(rval) = rsplode {
                        right.explode_right(rval);
                    }
                    return Some((lsplode, None));
                }
                else if let Some((lsplode, rsplode)) = right.explode_depth(depth + 1) {
                    if let Some(lval) = lsplode {
                        left.explode_left(lval);
                    }
                    return Some((None, rsplode));
                }
                None
            }
        }
    }

    fn explode_left(&mut self, value: u32) {
        use SnailNum::*;
        match self {
            Number(v) => { *v += value; }
            Pair(_, right) => { right.explode_left(value); }
        }
    }

    fn explode_right(&mut self, value: u32) {
        use SnailNum::*;
        match self {
            Number(v) => { *v += value; }
            Pair(left, _) => { left.explode_right(value); }
        }
    }

    fn split(&mut self) -> bool {
        use SnailNum::*;
        match self {
            &mut Number(n) if n > 9 => {
                let left = n / 2;
                let right = n - left;
                *self = SnailNum::pair(Number(left), Number(right));
                true
            }
            Number(_) => false,
            Pair(left, right) => left.split() || right.split(),
        }
    }

    fn magnitude(&self) -> u32 {
        use SnailNum::*;
        match self {
            Number(n) => *n,
            Pair(left, right) => left.magnitude() * 3 + right.magnitude() * 2,
        }
    }
}

impl fmt::Debug for SnailNum {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Number(n) => write!(f, "{}", n),
            Self::Pair(a, b) =>
                write!(f, "[{:?},{:?}]", a, b),
        }
    }
}

fn part1() -> io::Result<()> {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().collect::<Result<Vec<String>, _>>()?;
    let answer = lines.iter()
        .map(SnailNum::from_line)
        .reduce(SnailNum::add)
        .unwrap();
    println!("{}", answer.magnitude());
    Ok(())
}

fn part2() -> io::Result<()> {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().collect::<Result<Vec<String>, _>>()?;
    let nums: Vec<_> = lines.iter().map(SnailNum::from_line).collect();

    let mut magnitude = 0;
    for (i, num1) in nums.iter().enumerate() {
        for (j, num2) in nums.iter().enumerate() {
            if i == j { continue; }
            let sum_magnitude = SnailNum::add(num1.clone(), num2.clone()).magnitude();
            magnitude = magnitude.max(sum_magnitude);
        }
    }
    println!("{}", magnitude);
    Ok(())
}

fn main() -> io::Result<()> {
    match env::args().nth(1).as_deref() {
        Some("part1") => part1()?,
        Some("part2") => part2()?,
        Some(word) => { eprintln!("Please specify 'part1' or 'part2', not {:?}", word); }
        None => { eprintln!("Please specify 'part1' or 'part2'"); }
    }
    Ok(())
}
