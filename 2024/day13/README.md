# Day 13: Claw Contraption

## Usage

```bash
cargo run --bin day13 part1 < input.txt
cargo run --bin day13 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/13))

The problem gives us a bunch of discrete test cases describing strange claw machines.
Each claw machine has two buttons, A and B, which each move the claw by some X and Y amount.
Pressing A costs 3 tokens, pressing B costs 1 token.
We're also told the coordinate of the prize.
We want to get as many prizes as possible, and are asked the least number of tokens we can spend to get them.

The answer for my input in **part 1** is 39996.

In **part 2** we add 10000000000000 to each prize component and solve again.
The answer for my input is 73267584326867.

## Retrospective

For part 1 I iterated over values for `b` to find the smallest working answer, using arithmetic to check if there existed an `a` that would work.
When it became clear in part 2 that iterating over the possibilities wasn't going to be feasible, I recognized fairly quickly that I had two linear equations with two unknowns.
It's been a while since I've had to do linear algebra, but I thought I might be able to fake my way through it.
I was not able!
Had to look up how to solve a matrix.
Luckily this is fairly methodical for a 2x2 matrix, so this wasn't so bad.
I was worried we were going to run into integer overflow or rounding errors, but neither came up.

I didn't expect Advent of Code would make me re-learn linear algebra, so this was pretty neat!
I'm grateful my input did not contain buttons with the same slope!
