# Day 4: Ceres Search

## Usage

```bash
cargo run --bin day04 part1 < input.txt
cargo run --bin day04 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/3))

**Part 1** gives us a word search: we're searching for the total count of the word `XMAS`.
The answer for my input is 2573.

**Part 2** has us search instead for occurences of the word `MAS`, crossed with itself in an X pattern.
The answer for my input is 1850.

## Retrospective

Fun little problem.
My code feels a lot like some Python code I've written a few times, though Rust is a bit more verbose when working with iterators in this particular way.
I really like the pattern of defining iterators of directions and zipping them to check for the shapes we care about.

Not much else to say.
Fun day!
