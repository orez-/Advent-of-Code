# Day 10: Hoof It

## Usage

```bash
cargo run --bin day10 part1 < input.txt
cargo run --bin day10 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/10))

We're asked to find paths through a grid which step through all ten consecutive digits.

In **part 1** we're asked to count unique start/end combos.
The answer for my input is 737.

In **part 2** we're asked to count paths.
The answer for my input is 1619.

## Retrospective

Standard graph search.
Went for the recursive solution, despite mentioning the other day that I don't usually reach for recusion.
I don't know why.

I misread the problem and actually ended up implementing part 2 before part 1, without knowing what part 2 would be.
This made the part 2 an easy solve: I just hit undo a bunch.
