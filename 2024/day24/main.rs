use std::array::TryFromSliceError;
use std::collections::{BTreeMap, BTreeSet};
use std::env;
use std::io::{self, BufRead};

mod debug;

#[derive(Copy, Clone, Ord, PartialOrd, Hash, Eq, PartialEq)]
struct Gate([u8; 3]);
impl TryFrom<&str> for Gate {
    type Error = TryFromSliceError;
    fn try_from(s: &str) -> Result<Gate, TryFromSliceError> {
        let bytes: [u8; 3] = s.as_bytes().try_into()?;
        Ok(Gate(bytes))
    }
}

#[derive(Copy, Clone, Ord, PartialOrd, Hash, Eq, PartialEq)]
struct Equation {
    left: Gate,
    op: BinOp,
    right: Gate,
    out: Gate,
}

#[derive(Copy, Clone, Ord, PartialOrd, Hash, Eq, PartialEq)]
enum BinOp {
    And,
    Or,
    Xor,
}

struct Input {
    vars: BTreeMap<Gate, bool>,
    equations: Vec<Equation>,
}

fn part1(input: Input) -> u64 {
    let mut vars: BTreeMap<Gate, bool> = input.vars;
    let mut inbox = [const { BTreeSet::new() }; 3];
    let mut eqn_lookup: BTreeMap<Gate, Vec<Equation>> = BTreeMap::new();

    for gate in input.equations {
        let idx =
            !vars.contains_key(&gate.left) as usize +
            !vars.contains_key(&gate.right) as usize;
        eqn_lookup.entry(gate.left).or_default().push(gate);
        eqn_lookup.entry(gate.right).or_default().push(gate);
        inbox[idx].insert(gate);
    }

    while let Some(gate) = inbox[0].pop_last() {
        let left = vars[&gate.left];
        let right = vars[&gate.right];
        let val = match gate.op {
            BinOp::And => left && right,
            BinOp::Or => left || right,
            BinOp::Xor => left ^ right,
        };
        vars.insert(gate.out, val);
        let Some(eqns) = eqn_lookup.get(&gate.out) else { continue };
        for &eqn in eqns {
            // fortunately there's no `a ? a = b`
            if inbox[2].remove(&eqn) {
                inbox[1].insert(eqn);
            } else if inbox[1].remove(&eqn) {
                inbox[0].insert(eqn);
            }
        }
    }
    vars.iter().rev().filter(|(k, _)| k.0[0] == b'z').fold(0, |a, (_, &b)| (a << 1) | (b as u64))
}

fn part2(input: Input) -> i32 {
    let _ = input;
    0
}

fn read_lines() -> io::Result<Input> {
    let mut vars = BTreeMap::new();
    let mut equations = Vec::new();
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();
    for line in lines.by_ref().take_while(|line| !line.as_ref().is_ok_and(|line| line.is_empty())) {
        let [g0, g1, g2, _, _, b] = line?.into_bytes().try_into().unwrap();
        let gate = Gate([g0, g1, g2]);
        let bit = b == b'1';
        vars.insert(gate, bit);
    }
    for line in lines {
        let line = line?;
        let pieces: Vec<_> = line.split_ascii_whitespace().collect();
        let [a, op, b, _, c] = pieces.try_into().unwrap();
        let op = match op {
            "AND" => BinOp::And,
            "OR" => BinOp::Or,
            "XOR" => BinOp::Xor,
            _ => panic!(),
        };
        let left: Gate = a.try_into().unwrap();
        let right: Gate = b.try_into().unwrap();
        let out: Gate = c.try_into().unwrap();
        equations.push(Equation { left, op, right, out });
    }
    Ok(Input { vars, equations })
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
