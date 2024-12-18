# Day 18: RAM Run

## Usage

```bash
cargo run --bin day18 part1 < input.txt
cargo run --bin day18 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/18))

Today's problem has us navigate a maze.

**Part 1** wants to know the length of the fastest path through the maze, considering the first 1024 obstacles.
The answer for my input is 436.

**Part 2** wants to know the smallest of the obstacle list which results in an unsolvable maze.
Specifically it asks the coordinate of the first obstacle which makes the maze unsolvable.
The answer for my input is 61,50.

## Retrospective

More mazes!
Works for me.

For part 2 I went for a binary search to find the cutoff point where the maze becomes unsolvable.
Conveniently I already had the obstacles kept as a mapping from coordinates to the time they appear: I was expecting we were going to need to solve the maze _as_ the obstacles were appearing.
But instead this let me reuse the input set for cheap.
It's a constant lookup for if a cell is both in our obstacle set and if it's less than the cutoff time we're considering.
