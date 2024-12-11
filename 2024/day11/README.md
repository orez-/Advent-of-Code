# Day 11: Plutonian Pebbles

## Usage

```bash
cargo run --bin day11 part1 < input.txt
cargo run --bin day11 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/11))

We have a bunch of magic stones which grow and split based on specific rules.
We're asked to count how many stones exist after some number of iterations.

In **part 1** we iterate 25 times.
The answer for my input is 186175.

In **part 2** we iterate 75 times.
The answer for my input is 220566831337810.

## Retrospective

I love a problem that has you do the simple thing x times, and then forces you to come up with a better approach to do it x + y times.
Part 1 explicitly calls out that the order of the stones matters, but this is a misdirect: order absolutely does not matter.
We can track stones in a Counter to avoid recalculating the same stone value multiple times in a single blink.

I sure wish Rust had a better story for returning a different number of values from a `flat_map`.
For part 1 each stone mapped to one or two stones, but:
- You can't return an array from the `flat_map`, since all returned arrays need to have the same size
- You can't construct and return a slice, since it doesn't live long enough, I think.
- You can return a `Vec`, but it needs to allocate for each stone.
- Could return an [`itertools::Either`](https://docs.rs/itertools/latest/itertools/enum.Either.html), or construct your own enum which implements Iterator. That's a lot of boilerplate to accomplish this!
- Since we're immediately `collect`ing the result into a `Vec` anyway, in this case we could skip `flat_map` all together and `extend` elements into a mutable `Vec` directly. This isn't a bad option.

Ended up going with returning `Vec` in the `flat_map`, but like. Oof!
