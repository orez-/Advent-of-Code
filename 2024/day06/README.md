# Day 6: Guard Gallivant

## Usage

```bash
cargo run --bin day06 part1 < input.txt
cargo run --bin day06 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/6))

Today's problem has us simulating walking a grid.
The guard in the grid walks straight until she hits an obstacle, then turns right.
**Part 1** asks us to find how many tiles she walks on before exiting the grid.
The answer for my input is 5453.
**Part 2** has us add a single obstacle to the grid in order to trap the guard in a loop, and asks how many positions we could choose from in order to do so.
The answer for my input is 2188.

## Retrospective

Good grid walk problem.
Pretty standard.
The usual tricks apply: track direction as `dx` and `dy` for simplicity, look before you leap, leverage `usize` to only have to do one bounds check in each axis.

My first solution for part 2 ended up taking 6 seconds in `--release` mode, which is acceptable when finding a solution, but still higher than I'd expect to see for a Day 6!
I was checking every empty cell to see if adding an obstacle would help, but thinking about it more we only need to check cells that the guard is going to hit.. which is exactly what we found in part 1!
Changing this check to just use the answer from part 1 has this run in around a second, which is much better.
I also went through and factored the grid walking code into a common function.
I'm not sure if this is simpler or better (I probably wouldn't use this code for something I needed to maintain), but it's kind of neat at least.

During the initial solve, for part 2 I remembered to clear the `seen` set, but forgot to reset the guard position for a bit.
Oh well.
