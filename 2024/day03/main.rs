use std::env;
use std::io::{self, BufRead};
use regex::Regex;

fn part1(corpus: String) -> i32 {
    let mut corpus = corpus.as_str();
    let mut total = 0;
    while let Some(pos) = corpus.find("mul(") {
        corpus = &corpus[pos+4..];
        let Some(prefix) = corpus.chars().take(4).position(|c| c == ',') else { continue };
        let Ok(a): Result<i32, _> = corpus[..prefix].parse() else { continue };
        corpus = &corpus[prefix+1..];
        let Some(suffix) = corpus.chars().take(4).position(|c| c == ')') else { continue };
        let Ok(b): Result<i32, _> = corpus[..suffix].parse() else { continue };
        total += a * b;
    }
    total
}

fn part2(corpus: String) -> i32 {
    let mut corpus = corpus.as_str();
    let chunks = std::iter::from_fn(|| {
        if corpus.is_empty() { return None }
        let Some((do_mul, next)) = corpus.split_once("don't()") else {
            let out = Some(corpus);
            corpus = "";
            return out;
        };
        corpus = next.split_once("do()").map_or("", |(_, next)| next);
        Some(do_mul)
    });

    let mut total = 0;
    for mut corpus in chunks {
        while let Some(pos) = corpus.find("mul(") {
            corpus = &corpus[pos+4..];
            let Some(prefix) = corpus.chars().take(4).position(|c| c == ',') else { continue };
            let Ok(a): Result<i32, _> = corpus[..prefix].parse() else { continue };
            corpus = &corpus[prefix+1..];
            let Some(suffix) = corpus.chars().take(4).position(|c| c == ')') else { continue };
            let Ok(b): Result<i32, _> = corpus[..suffix].parse() else { continue };
            total += a * b;
        }
    }
    total
}

fn part1_re(corpus: String) -> i32 {
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
    let mut total = 0;
    for (_, [a, b]) in re.captures_iter(&corpus).map(|c| c.extract()) {
        let a: i32 = a.parse().unwrap();
        let b: i32 = b.parse().unwrap();
        total += a * b;
    }
    total
}

fn part2_re(corpus: String) -> i32 {
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)|don't\(\)|do\(\)").unwrap();
    let mut total = 0;
    let mut do_mul = true;
    for cap in re.captures_iter(&corpus) {
        match cap.get(0).map(|m| m.as_str()) {
            Some("don't()") => do_mul = false,
            Some("do()") => do_mul = true,
            Some(_) if do_mul => {
                let a: i32 = cap.get(1).unwrap().as_str().parse().unwrap();
                let b: i32 = cap.get(2).unwrap().as_str().parse().unwrap();
                total += a * b;
            }
            _ => (),
        }
    }
    total
}

fn read_lines() -> io::Result<String> {
    let stdin = io::stdin();
    Ok(stdin.lock().lines().collect::<io::Result<Vec<_>>>()?.join("\n"))
}

fn main() -> io::Result<()> {
    match env::args().nth(1).as_deref() {
        Some("part1") => println!("{}", part1(read_lines()?)),
        Some("part2") => println!("{}", part2(read_lines()?)),
        Some("part1_re") => println!("{}", part1_re(read_lines()?)),
        Some("part2_re") => println!("{}", part2_re(read_lines()?)),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
    Ok(())
}
