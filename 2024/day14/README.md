# Day 14: Restroom Redoubt

## Usage

```bash
cargo run --bin day14 part1 < input.txt
cargo run --bin day14 part2 < input.txt
```

Note that part 2 runs forever.
You'll need to ctrl+c to halt it.

## Problem Summary ([?](https://adventofcode.com/2024/day/14))

We're given a bunch of positions and velocities of guard robots.
The robots will loop over the edges of the grid.

**Part 1** asks us to simulate the robots for 100 steps, and asks us to multiply the counts of robots in each quadrant.
The answer for my input in **part 1** is 226179492.

In **part 2** we're asked to find the first time where the bots resemble a Christmas tree(!?).
The answer for my input is 7502.

## Retrospective

For part 2, I noticed that a bunch of bots seemed to clump horizontally every `t = 101x + 28`, so I tried just printing those results, and sure enough the tree appeared at 7502.
I was hesitant to try to come up with a heuristic to try to recognize trees programatically: I wasn't sure if the image was going to try to use clumps of bots as ornaments, or something.
But this worked well enough.

Cute problem!
Gotta do something to combat ChatGPT dominating the leaderboards, I guess.
