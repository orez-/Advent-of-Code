use std::env;
use std::io::{self, BufRead};

fn part1(lines: Vec<String>) -> u64 {
    let [numbers @ .., ops] = lines.as_slice() else { panic!() };
    let ops: Vec<_> = ops.split_ascii_whitespace().map(|op| match op {
        "+" => false,
        "*" => true,
        _ => panic!("unexpected op {op}"),
    }).collect();
    let mut out: Vec<_> = ops.iter().map(|&op| op as u64).collect();
    for line in numbers {
        for (idx, num) in line.split_ascii_whitespace().map(|elem| elem.parse::<u64>().expect("number")).enumerate() {
            if ops[idx] {
                out[idx] *= num;
            } else {
                out[idx] += num;
            }
        }
    }
    out.iter().sum()
}

fn part2(mut lines: Vec<String>) -> u64 {
    let Some(ops) = lines.pop() else { panic!("no ops?") };
    let mut numbers: Vec<_> = lines.iter().map(|line| line.as_bytes()).collect();
    let mut lens: Vec<_> = ops.split(['+', '*']).skip(1).map(|slice| slice.len()).collect();
    *lens.last_mut().expect("at least one op") += 1;
    let ops = ops.split_ascii_whitespace().map(|op| match op {
        "+" => false,
        "*" => true,
        _ => panic!("unexpected op {op}"),
    });

    ops.zip(lens).fold(0, |agg, (is_mul, len)| {
        let mut streams: Vec<_> = numbers
            .iter_mut()
            .map(|row| {
                let num = row.split_off(..len).expect("correct size");
                row.split_off_first();
                // println!("{}", str::from_utf8(num).unwrap());
                num.iter().rev()
            })
            .collect();
        let mut total = is_mul as u64;
        for _ in 0..len {
            let mut num = 0;
            for stream in &mut streams {
                let Some(&byte) = stream.next() else { break };
                if byte == b' ' { continue };
                num *= 10;
                num += (byte - b'0') as u64;
            }

            if is_mul {
                total *= num;
            } else {
                total += num;
            }
        }
        agg + total
    })
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
