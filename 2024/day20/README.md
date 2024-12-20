# Day 20: Race Condition

## Usage

```bash
cargo run --bin day20 part1 < input.txt
cargo run --release --bin day20 part2 < input.txt
```

Part 2 is a little slow without the `--release` flag.

## Problem Summary ([?](https://adventofcode.com/2024/day/20))

We're given a maze with a single track, and we're told we're allowed to cheat once through walls.
We're asked how many different cheats would save us at least 100 steps.

**Part 1** allows us to cheat through walls for 2 steps (ie: through one wall).
The answer for my input is 1454.

**Part 2** allows us to cheat through walls for 20 (consecutive) steps.
The answer for my input is 997879.

## Retrospective

Another maze!
A unicursal maze this time!

For part 1, I keep track of our progress along the maze at each position, then check each of those positions to the east and south to see if jumping the wall (in either direction) would be beneficial enough to note.

For part 2 I considered ways to find a solution quickly: some way of reusing region information between cells.
In the end I decided to just try checking the cartesian product of maze cells.
With 9421 maze cells, I calculated that this would be on the order of ~90M comparisons, which felt kind of high.
But release-mode Rust solved this no problem.
