# Day 12: Garden Groups

## Usage

```bash
cargo run --bin day12 part1 < input.txt
cargo run --bin day12 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/12))

We're asked to fence off regions in a grid.
The score for each region is the number of fence segments times the total area.
The score for the grid is the sum of scores for all regions.

In **part 1** each fence segment counts once.
The answer for my input is 1461806.

In **part 2** each contiguous line of fences in a single direction counts once.
The answer for my input is 887932.

## Retrospective

Hey! I've [done this before!](https://github.com/orez-/alphgen/blob/e1859ba4475cf88b044c6c9d79205adc189718d8/src/sprite.rs#L19-L73)

Good problem.
Instead of trying to walk the perimeter, I like the trick of toggling the edges of each grid cell.
If an edge gets toggled twice, that means both sides are in the same region and this edge is not in the perimeter.

This worked well for part 1, but in part 2 I got bit by the "Be especially careful" part of the problem description: a fence going left should not connect to a fence going right ([not again!](https://github.com/orez-/alphgen/commit/f77d50577e24e870df9fb610374cf8b3da29e1e2)).
Ended up creating a whole-dang `Edge` and `Direction` type to make modeling this easier.
Had to spend some time debugging a typo (I had left and right's reverse positions swapped), but otherwise went pretty smoothly.
