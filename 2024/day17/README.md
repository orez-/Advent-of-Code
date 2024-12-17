# Day 17: Chronospatial Computer

## Usage

```bash
cargo run --bin day17 part1 < input.txt
cargo run --bin day17 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/17))

Problem input is an opcode language with three registers.
See the problem definition for the specifics of what these opcodes do.

**Part 1** has us run the initial program and collect the output.
The answer sequence for my input is `2,0,7,3,0,3,1,3,7`.

**Part 2** wants to know the smallest initial value of register A to make our program output itself.
The answer for my input is `247839539763386`.

## Retrospective

Very cool problem.
Advent of Code has done problems where you need to analyze some opcode, but this is the first one I've done where writing code actually helped, where analyzing the code by hand was too convoluted.

My input program looks something like this:

```c#
do {
  b = a & 0b111
  b ^= 1
  c = a / (1 << b)
  a >>= 3
  b ^= c
  b ^= 6
  print(b & 0b111)
} while a != 0
```

(I suspect the `b` xors are the only difference between inputs for other people).

In particular, the interaction between the registers with the `c = a / (1 << b)` makes the whole program difficult to reason about.
But we can see that for the final iteration, we know `a` is in the range `1` to `8` (since it becomes 0 when we `a >>= 3`), so we can check each possible value and see if it produces the correct final digit in the output.
And once these first three bits are locked down, we can similarly check for the next three bits in the range `1` to `8`, and so on.

The only trick at this point is some sets of three bits have multiple possible answers which give the correct output, but we can graph search these results to find the best one.
