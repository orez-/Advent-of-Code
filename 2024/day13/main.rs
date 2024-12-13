use regex::Regex;
use std::env;
use std::io::{self, BufRead};

type Coord = [i64; 2];
struct Game {
    a: Coord,
    b: Coord,
    prize: Coord,
}

fn part1(games: Vec<Game>) -> i64 {
    let mut cost = 0;
    for game in games {
        for b in (0..=100).rev() {
            let ax = game.prize[0] - game.b[0] * b;
            let ay = game.prize[1] - game.b[1] * b;
            if ax < 0 || ay < 0 { continue }
            if ax % game.a[0] != 0 || ay % game.a[1] != 0 { continue }
            if ax / game.a[0] != ay / game.a[1] { continue }
            cost += (ax / game.a[0]) * 3 + b;
            break;
        }
    }
    cost
}

fn part2(games: Vec<Game>) -> i64 {
    let mut cost = 0;
    for mut game in games {
        game.prize[0] += 10000000000000;
        game.prize[1] += 10000000000000;

        // linear algebra!?
        let det = (game.a[0] * game.b[1]) - (game.a[1] * game.b[0]);
        let big_a = game.b[1] * game.prize[0] - game.b[0] * game.prize[1];
        let big_b = -game.a[1] * game.prize[0] + game.a[0] * game.prize[1];
        if (big_a < 0) != (big_b < 0) || big_a % det != 0 || big_b % det != 0 { continue }
        let a = big_a / det;
        let b = big_b / det;
        cost += a * 3 + b;
    }
    cost
}

fn read_lines() -> io::Result<Vec<Game>> {
    let stdin = io::stdin();
    let lines: Result<Vec<_>, _> = stdin.lock().lines().collect();
    let lines = lines?;
    let re = Regex::new(r"X.(\d+), Y.(\d+)").unwrap();
    let parse_line = |s| re.captures(s).unwrap().extract().1.map(|c| c.parse().unwrap());
    let games = lines.chunks(4).map(|chunk| Game {
        a: parse_line(&chunk[0]),
        b: parse_line(&chunk[1]),
        prize: parse_line(&chunk[2]),
    }).collect();
    Ok(games)
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
