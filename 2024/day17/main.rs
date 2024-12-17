use std::env;
use std::io::{self, BufRead};

#[derive(Clone)]
struct Program {
    a: u64,
    b: u64,
    c: u64,
    program: Vec<u8>,
    ip: usize,
}

impl Program {
    fn step(&mut self) -> Result<Option<u64>, ()> {
        match self.instr()? {
            0 => self.a /= 1 << self.combo()?,
            1 => self.b ^= self.literal()?,
            2 => self.b = self.combo()? & 0b111,
            3 => if self.a != 0 { self.ip = self.literal()? as _ },
            4 => {
                self.instr()?;
                self.b ^= self.c;
            }
            5 => return Ok(Some(self.combo()? & 0b111)),
            6 => self.b = self.a / (1 << self.combo()?),
            7 => self.c = self.a / (1 << self.combo()?),
            _ => panic!(),
        }
        Ok(None)
    }

    fn literal(&mut self) -> Result<u64, ()> {
        Ok(self.instr()? as u64)
    }

    fn combo(&mut self) -> Result<u64, ()> {
        let val = match self.instr()? {
            c @ 0..=3 => c as u64,
            4 => self.a,
            5 => self.b,
            6 => self.c,
            _ => panic!(),
        };
        Ok(val)
    }

    fn instr(&mut self) -> Result<u8, ()> {
        if self.ip >= self.program.len() { return Err(()) }
        let out = self.program[self.ip];
        self.ip += 1;
        Ok(out)
    }
}

fn part1(mut program: Program) -> String {
    let mut out = Vec::new();
    while let Ok(val) = program.step() {
        if let Some(val) = val {
            out.push(val.to_string());
        }
    }
    out.join(",")
}

fn part2(initial_program: Program) -> u64 {
    let mut out = Vec::new();
    let mut frontier = std::collections::VecDeque::from([0]);
    while let Some(a) = frontier.pop_front() {
        let a = a << 3;
        for a in a..a + 8 {
            out.clear();
            let mut program = initial_program.clone();
            program.a = a;

            while let Ok(val) = program.step() {
                if let Some(val) = val {
                    out.push(val as u8);
                }
            }

            if out == initial_program.program {
                return a;
            }
            if initial_program.program.ends_with(&out) {
                frontier.push_back(a);
            }
        }
    }
    unreachable!()
}

fn read_lines() -> io::Result<Program> {
    let stdin = io::stdin();
    let lines: Result<Vec<_>, _> = stdin.lock().lines().take(5).collect();
    let [a, b, c, _, program] = lines?.try_into().unwrap();
    let a = a.split_once(": ").unwrap().1.parse().unwrap();
    let b = b.split_once(": ").unwrap().1.parse().unwrap();
    let c = c.split_once(": ").unwrap().1.parse().unwrap();
    let program = program.split_once(": ").unwrap().1.split(",");
    let program = program.map(|x| x.parse().unwrap()).collect();
    Ok(Program { a, b, c, program, ip: 0 })
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
