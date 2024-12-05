use std::collections::{HashMap, HashSet};
use std::env;
use std::io::{self, BufRead};

fn parse_input(lines: Vec<String>) -> (HashMap<i32, Vec<i32>>, Vec<Vec<i32>>) {
    // `split_once` is unstable as of 1.83
    let split: Vec<_> = lines.split(|line| line.is_empty()).collect();
    let [constraint_lines, test_lines] = split.try_into().unwrap();
    let mut constraints: HashMap<_, Vec<_>> = HashMap::new();
    for line in constraint_lines {
        let (a, b) = line.split_once('|').unwrap();
        let a = a.parse::<i32>().unwrap();
        let b = b.parse::<i32>().unwrap();
        constraints.entry(a).or_default().push(b);
    }
    let tests = test_lines
        .into_iter()
        .map(|line| line.split(',').map(|x| x.parse().unwrap()).collect())
        .collect();
    (constraints, tests)
}

fn part1(lines: Vec<String>) -> i32 {
    let (constraints, tests) = parse_input(lines);
    tests
        .into_iter()
        .filter_map(|list| {
            let mut disallowed: HashSet<i32> = HashSet::new();
            for elem in list.iter().rev() {
                if disallowed.contains(&elem) {
                    return None;
                }
                if let Some(disallow) = constraints.get(&elem) {
                    disallowed.extend(disallow);
                }
            }
            Some(list[list.len()/2])
        })
        .sum()
}

fn part2(lines: Vec<String>) -> i32 {
    let (constraints, tests) = parse_input(lines);
    tests
        .into_iter()
        .filter_map(|mut list| {
            // this is extremely wasteful, but also the simplest to implement
            // as far as i can come up with.
            let mut needs_rearranging = false;
            let mut disallowed: HashMap<i32, usize> = HashMap::new();
            'again: loop {
                disallowed.clear();
                for (idx, elem) in list.iter().enumerate().rev() {
                    if let Some(&swap_idx) = disallowed.get(&elem) {
                        needs_rearranging = true;
                        list.swap(idx, swap_idx);
                        continue 'again;
                    }
                    if let Some(disallow) = constraints.get(&elem) {
                        for &num in disallow {
                            disallowed.insert(num, idx);
                        }
                    }
                }
                break;
            }
            needs_rearranging.then_some(list[list.len()/2])
        })
        .sum()
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
