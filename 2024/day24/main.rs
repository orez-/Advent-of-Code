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

impl Equation {
    fn sort(self) -> Self {
        if self.left < self.right {
            return self
        }
        Equation {
            left: self.right,
            op: self.op,
            right: self.left,
            out: self.out,
        }
    }
}

#[derive(Copy, Clone, Ord, PartialOrd, Hash, Eq, PartialEq, Debug)]
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

fn print_eqn(var: Gate, eqns: &BTreeMap<Gate, Equation>) -> String {
    let Some(eqn) = eqns.get(&var) else { return var.to_string() };
    let left = print_eqn(eqn.left, eqns);
    let right = print_eqn(eqn.right, eqns);
    if left < right {
        format!("({left} {} {right})", eqn.op)
    } else {
        format!("({right} {} {left})", eqn.op)
    }
}

#[derive(Default)]
struct Digits {
    z: Option<Gate>,
    dig: Option<Gate>,
    carry: Option<Gate>,
    pre: Option<Gate>,
    xiyi: Option<Gate>,
}

impl Digits {
    fn to_row(&self) -> String {
        let to_str = |g: Option<Gate>| g.map_or("-".to_string(), |g| g.to_string());
        format!("{}\t{}\t{}\t{}\t{}", to_str(self.z), to_str(self.dig), to_str(self.carry), to_str(self.pre), to_str(self.xiyi))
    }
}

fn part2(mut input: Input) -> String {
    let gate = |s: &str| s.try_into().unwrap();
    let x_gate = |idx: usize| gate(format!("x{idx:<02}").as_str());
    let y_gate = |idx: usize| gate(format!("y{idx:<02}").as_str());
    // let z_gate = |idx: usize| format!("z{idx:<02}").as_str().try_into().unwrap();

    let mut swap = |a, b| {
        let a = gate(a);
        let b = gate(b);
        let adx = input.equations.iter().position(|e| e.out == a).unwrap();
        let bdx = input.equations.iter().position(|e| e.out == b).unwrap();
        input.equations[adx].out = b;
        input.equations[bdx].out = a;
    };
    swap("fkb", "z16");
    swap("rqf", "nnr");
    swap("z31", "rdn");
    swap("z37", "rrn");

    let eqn_lookup: BTreeMap<_, _> = input
        .equations
        .into_iter()
        .map(|eqn| eqn.sort())
        .map(|eqn| ((eqn.left, eqn.op, eqn.right), eqn))
        .collect();

    let dig = eqn_lookup[&(x_gate(0), BinOp::Xor, y_gate(0))];
    let digits = Digits {
        z: Some(dig.out),
        dig: Some(dig.out),
        carry: None,
        ..Default::default()
    };
    println!("i\tzᵢ\tdigᵢ\tcarryᵢ\tpreᵢ\txᵢ&yᵢ");
    println!(" 0\t{}", digits.to_row());
    let mut addition_eqns = vec![digits];

    let lookup = |a, op, b| {
        let mut args = [a?, b?];
        args.sort_unstable();
        let [arg_a, arg_b] = args;
        Some(eqn_lookup.get(&(arg_a, op, arg_b))?.out)
    };

    // 45 but eh.
    for i in 1..=44 {
        let dig = eqn_lookup[&(x_gate(i), BinOp::Xor, y_gate(i))].out;
        let xiyi = eqn_lookup[&(x_gate(i - 1), BinOp::And, y_gate(i - 1))].out;
        let last = addition_eqns.last().unwrap();
        let pre = lookup(last.dig, BinOp::And, last.carry);
        let carry = if i == 1 { Some(xiyi) }
            else { lookup(Some(xiyi), BinOp::Or, pre) };
        let digits = Digits {
            z: lookup(Some(dig), BinOp::Xor, carry),
            dig: Some(dig),
            xiyi: Some(xiyi),
            pre,
            carry,
            ..Default::default()
        };
        println!("{i:>2}\t{}", digits.to_row());
        addition_eqns.push(digits);
    }

    let mut swaps = vec![
        "fkb", "z16",
        "rqf", "nnr",
        "z31", "rdn",
        "z37", "rrn",
    ];
    swaps.sort();
    swaps.join(",")
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
