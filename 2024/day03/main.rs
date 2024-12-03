use std::env;
use std::io::{self, BufRead};

fn part1(lines: Vec<String>) -> i32 {
    let corpus = lines.join("\n");
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

fn part2(lines: Vec<String>) -> i32 {
    let corpus = lines.join("\n");
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
