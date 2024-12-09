use std::collections::{BTreeMap, HashSet};
use std::env;
use std::io::{self, BufRead};

fn part1(corpus: String) -> usize {
    let mut corpus: Vec<_> = corpus.bytes().map(|b| (b - b'0') as usize).collect();
    if corpus.len() % 2 == 1 {
        corpus.push(0);
    }
    let mut checksum = 0_usize;
    let mut left_file_idx = 0;
    let mut right_file_idx = (corpus.len() - 2) / 2;
    let mut right_file = corpus[right_file_idx * 2];
    let mut actual_idx = 0;
    for chunk in corpus.chunks_exact(2) {
        if left_file_idx >= right_file_idx { break }
        // array_chunks is unstable as of 1.83
        let [file, mut gap] = chunk.try_into().unwrap();
        let geom: usize = (actual_idx..actual_idx + file).sum();
        checksum += left_file_idx * geom;
        actual_idx += file;

        left_file_idx += 1;
        while gap > 0 && left_file_idx < right_file_idx {
            if right_file > gap {
                right_file -= gap;
                let geom: usize = (actual_idx..actual_idx + gap).sum();
                checksum += right_file_idx * geom;
                actual_idx += gap;
                break;
            } else {
                gap -= right_file;
                let geom: usize = (actual_idx..actual_idx + right_file).sum();
                checksum += right_file_idx * geom;
                actual_idx += right_file;

                right_file_idx -= 1;
                right_file = corpus[right_file_idx * 2];
            }
        }
    }
    if right_file > 0 {
        let geom: usize = (actual_idx..actual_idx + right_file).sum();
        checksum += right_file_idx * geom;
    }
    checksum
}

#[derive(Debug, Clone, Copy)]
struct File {
    size: usize,
    id: usize,
}

// tried to make part 1 performant, to the detriment of comprehensibility.
// for part 2 i'm ready for it to be done.
fn part2(corpus: String) -> usize {
    let mut corpus: Vec<_> = corpus.bytes().map(|b| (b - b'0') as usize).collect();
    if corpus.len() % 2 == 1 {
        corpus.push(0);
    }
    let mut filesystem = BTreeMap::new();
    let mut right_edge = 0;
    for (id, chunk) in corpus.chunks_exact(2).enumerate() {
        let [size, gap] = chunk.try_into().unwrap();
        filesystem.insert(right_edge, File { size, id });
        right_edge += size + gap;
    }

    let mut seen = HashSet::new();
    let mut right = right_edge;
    while let Some((&file_position, &file)) = filesystem.range(..right).next_back() {
        right = file_position;
        let File { size, id } = file;
        if !seen.insert(id) { continue };

        // find a gap to fit it
        let mut gaps = filesystem
            .iter()
            .map(|(&start0, f0)| start0 + f0.size)
            .zip(filesystem.keys().copied().skip(1).chain([right_edge]));
        if let Some((pos, _)) = gaps.find(|(end0, start1)| start1 - end0 >= size).filter(|&(pos, _)| pos < file_position) {
            filesystem.remove(&file_position);
            filesystem.insert(pos, file);
        }
    }

    let mut checksum = 0;
    for (start, file) in filesystem {
        let geom: usize = (start..start + file.size).sum();
        checksum += file.id * geom;
    }
    checksum
}

fn read_line() -> io::Result<String> {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().collect::<io::Result<Vec<_>>>()?;
    let [line] = lines.try_into().unwrap();
    Ok(line)
}

fn main() -> io::Result<()> {
    match env::args().nth(1).as_deref() {
        Some("part1") => println!("{}", part1(read_line()?)),
        Some("part2") => println!("{}", part2(read_line()?)),
        Some(word) => eprintln!("Please specify 'part1' or 'part2', not {:?}", word),
        None => eprintln!("Please specify 'part1' or 'part2'"),
    }
    Ok(())
}
