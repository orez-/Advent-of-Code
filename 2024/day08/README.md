# Day 8: Resonant Collinearity

## Usage

```bash
cargo run --bin day08 part1 < input.txt
cargo run --bin day08 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/8))

The problem input describes a grid of radio towers of different frequencies.
Every two towers of the same frequency create "antinode" points.
We're asked to count the number of antinode points within the grid of the problem input.

In **part 1**, antinodes are colinear with the line of nodes, extended an even distance from the towers on either side.
The answer for my input is 320.

In **part 2** there are an infinite number of antinodes in both directions from the towers, spaced evenly at the distance between the towers.
The answer for my input is 1157.

## Retrospective

Nothing interesting to say today.
Found this fairly straightforward.
The way I setup part 1 allowed part 2 to flow naturally.

Sure wish [`checked_signed_diff`](https://doc.rust-lang.org/std/primitive.usize.html#method.checked_signed_diff) was stabilized.
