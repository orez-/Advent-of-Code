# Day 3: Mull It Over

## Usage

```bash
cargo run --bin day03 part1 < input.txt
cargo run --bin day03 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/3))

In **part 1**, we're searching for text of the form `mul(#,#)`, where each `#` is a one to three digit number.
We multiply these two numbers together and sum all such `mul`s to get the answer.
The answer for my input is 173731097.

In **part 2**, we also look for `do()` and `don't()` commands.
A `don't()` command prevents subsequent `mul(#,#)`s from contributing to the total, but a `do()` command re-enables further `mul(#,#)`s.
The answer for my input is 93729253.

## Retrospective

Oof!
I've never used a regex in Rust before, and I'm used to coding challenges that don't allow external crates, so I dived right in with a token-parsing approach instead.
Only when I got to the end did I realize that this probably would've been a good opportunity to learn the regex crate!

My solution for part 1 leverages `find` to find a `mul(` prefix, then painstakingly looks for the two numbers and their delimiters, prefix-truncating the corpus all along.
Part 2 contains this exact check as well, but calls it on the elements of an iterator yielding the chunks between `do()`s and `don't()`s.

I did go back afterward and implement the regex version: you can run these with the `part1_re` and `part2_re` subcommands.
They're _much_ easier to follow, in my opinion!
Instead of chunking the input and operating on each chunk, we just handle tokens in the order we find them, maintaining the `do` or `dont` state appropriately.

I didn't go so deep with the regex crate, but I think I like it!
[`extract()`](https://docs.rs/regex/1.11.1/regex/struct.Captures.html#method.extract) returning an unpackable array is very nice, though it falls apart when there aren't a constant number of captures (understandably).
Not totally sure what the idiomatic thing is to do in this case, but I'm looking forward to using it more and learning.
