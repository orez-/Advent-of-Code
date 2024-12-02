# Day 2: Red-Nosed Reports

## Usage

```bash
cargo run --bin day02 part1 < input.txt
cargo run --bin day02 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/2))

We're given a list of independent sequences: in order to be "safe", a sequence must be strictly increasing or decreasing and each step must differ by no more than three.
We're asked to count the number of safe sequences.
In **part 1** the answer for my input is 246.
**Part 2** allows us to remove up to one number from each sequence to make it safe.
The answer for my input is 318.

## Retrospective

Another fairly straightforward one.
Really just translating the steps as described directly, nothing tricky yet.
Excited for [`array_windows`](https://doc.rust-lang.org/std/vec/struct.Vec.html#method.array_windows) to stabilize someday.
Also learned there doesn't seem to be a `filter` method on iterators that can mutate the elements, which I hit when trying to split the row parsing `map` from the safety check in part 2.
We can't remove (and immediately readd) elements from the sequence within a `filter`.
It turned out to flow nicer when we construct the `mut row` in the `filter` fn anyway, but that's an interesting Rust gotcha.
