use std::collections::*;
use std::env;
use std::fmt;
use std::io::{self, BufRead};

#[derive(Copy, Clone, Ord, PartialOrd, Hash, Eq, PartialEq)]
struct Ip([u8; 2]);

impl fmt::Display for Ip {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", std::str::from_utf8(&self.0).unwrap())
    }
}

fn part1(lines: Vec<(Ip, Ip)>) -> usize {
    let mut links: HashMap<Ip, Vec<Ip>> = HashMap::new();
    for (a, b) in lines {
        let (a, b) = (a.min(b), a.max(b));
        links.entry(a).or_default().push(b);
        links.entry(b).or_default();
    }
    links.values_mut().for_each(|v| v.sort_unstable());

    let mut tris = 0;
    for (n0, nexts) in &links {
        for (idx, n2) in nexts.iter().enumerate() {
            for n1 in &nexts[..idx] {
                if links[n1].binary_search(n2).is_ok() {
                    if n0.0[0] == b't' || n1.0[0] == b't' || n2.0[0] == b't' {
                        tris += 1;
                    }
                }
            }
        }
    }
    tris
}

type IpSet = BTreeSet<Ip>;
type Links = HashMap<Ip, IpSet>;

fn find_pentagram(
    links: &Links,
    required: &mut IpSet,
    potential: &IpSet,
    checked: Ip,
    best: &mut IpSet,
) {
    if required.len() > best.len() {
        *best = required.clone();
    }
    for &node in potential.range(checked..).skip_while(|&&c| c == checked) {
        let nexts = &links[&node];
        // can't fit in
        if !nexts.is_superset(required) {
            continue;
        }
        required.insert(node);
        let mut potential = potential & nexts;
        potential.remove(&node);

        find_pentagram(links, required, &potential, node, best);

        required.remove(&node);
    }
}

fn part2(lines: Vec<(Ip, Ip)>) -> String {
    let mut links: Links = Links::new();
    for (a, b) in lines {
        links.entry(a).or_default().extend([a, b]);
        links.entry(b).or_default().extend([a, b]);
    }

    let mut best = IpSet::new();
    let mut required = IpSet::new();
    let potential: IpSet = links.keys().copied().collect();
    find_pentagram(&links, &mut required, &potential, Ip(*b"@@"), &mut best);
    best.into_iter().map(|ip| ip.to_string()).collect::<Vec<_>>().join(",")
}

fn read_lines() -> io::Result<Vec<(Ip, Ip)>> {
    let stdin = io::stdin();
    stdin.lock().lines().map(|line| {
        let [a, b, _, c, d] = line?.into_bytes().try_into().unwrap();
        Ok((Ip([a, b]), Ip([c, d])))
    }).collect()
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
