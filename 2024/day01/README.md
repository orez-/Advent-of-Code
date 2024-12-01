# Day 1: Historian Hysteria

## Usage

```bash
cargo run --bin day01 part1 < input.txt
cargo run --bin day01 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/1))

Take the input as two columns of integers.
In **part 1**, we sort each list and sum the absolute difference between each pair.
The answer for my input is 2815556.
In **part 2**, we multiply each number in the left list by its occurences in the right list.
The answer for my input is 23927637.

## Retrospective

Been a few years since I've committed to an Advent of Code, so my goal for this year is to just finish each day.
Probably in Rust.
I like Rust.

Not much to say about a day 1.
I'm not speed-solving, but I am trying to solve the problem with minimal effort.
From that perspective, I ended up writing less-idiomatic Rust to parse the input.
Which felt bad!
Maybe I should've put together some input parsing helpers before today, or looked into input-parsing libraries.
