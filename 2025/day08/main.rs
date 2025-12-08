use std::env;
use std::io::{self, BufRead};
use crate::disjoint_set::DisjointSet;

mod disjoint_set;

fn part1(lines: Vec<String>) -> usize {
    let junctions: Vec<[u64; 3]> = lines.into_iter().map(|line| {
        let coords: Vec<u64> = line.split(',').map(|bit| bit.parse().expect("num")).collect();
        coords.try_into().expect("three")
    }).collect();

    let mut dists = Vec::new();
    for (idx0, &[x0, y0, z0]) in junctions.iter().enumerate() {
        for (idx1, &[x1, y1, z1]) in junctions[..idx0].iter().enumerate() {
            let dist = x0.abs_diff(x1).pow(2) + y0.abs_diff(y1).pow(2) + z0.abs_diff(z1).pow(2);
            dists.push((dist, idx0, idx1));
        }
    }

    let mut forest = DisjointSet::new();
    for idx in 0..junctions.len() {
        forest.insert(idx);
    }

    let (dists, _, _) = dists.select_nth_unstable(1000);
    for (_, idx0, idx1) in dists {
        forest.merge(*idx0, *idx1);
    }
    let mut groups: Vec<_> = forest.into_groups().map(|grp| grp.len()).collect();
    let (lens, _, _) = groups.select_nth_unstable_by(3, |a, b| b.cmp(a));
    lens.into_iter().fold(1, |a, b| a * *b)
}

fn part2(lines: Vec<String>) -> u64 {
    let junctions: Vec<[u64; 3]> = lines.into_iter().map(|line| {
        let coords: Vec<u64> = line.split(',').map(|bit| bit.parse().expect("num")).collect();
        coords.try_into().expect("three")
    }).collect();

    let mut dists = Vec::new();
    for (idx0, &[x0, y0, z0]) in junctions.iter().enumerate() {
        for (idx1, &[x1, y1, z1]) in junctions[..idx0].iter().enumerate() {
            let dist = x0.abs_diff(x1).pow(2) + y0.abs_diff(y1).pow(2) + z0.abs_diff(z1).pow(2);
            dists.push((dist, idx0, idx1));
        }
    }

    let mut forest = DisjointSet::new();
    for idx in 0..junctions.len() {
        forest.insert(idx);
    }

    dists.sort_unstable();
    let mut last = [0, 0];
    for (_, idx0, idx1) in dists {
        if forest.merge(idx0, idx1) {
            last = [idx0, idx1];
        }
    }
    let [a, b] = last;
    junctions[a][0] * junctions[b][0]
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
