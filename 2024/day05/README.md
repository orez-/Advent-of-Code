# Day 5: Print Queue

## Usage

```bash
cargo run --bin day05 part1 < input.txt
cargo run --bin day05 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/5))

We're given two sets of data.
The first is a set of ordering constraints, describing when some number must not appear after another number.
The second is a set of test cases: each line is an ordered list of numbers.
We're tasked with identifying test cases which are disordered per our ordering constraints.

**Part 1** has us sum the middle value of the **organized** tests.
The answer for my input is 5452.

**Part 2** has us reorder the disorganized tests to be ordered, specifically by swapping only the disordered entries, and summing the middle value of these.
The answer for my input is 4598.

## Retrospective

Good problem!

Part 1 was fairly straightforward: keep the mapping of constraints from `{first: second}`, then iterate each test case backwards.
When we find a `first` we add `second` to a list of `disallowed` values, and if we find a `disallowed` value then we're disorganized.

Part 2 was a little trickier.
I'm honestly not sure how tricky the test cases actually were, but theoretically reordering two entries may cause further entries to become disordered.
Decided to solve this in a not-very-efficient but simple way: when we encounter two disordered elements, we swap them and then restart the test case check from the beginning.

In general I'm not totally convinced the reordering rules as described are necessarily deterministic!
Consider:

```
1|2
1|3
321
```

All elements of this test case are disordered, so sorting them as `123` or `132` are both valid, and give different results.
I suppose the input file was designed so this wouldn't happen, but I definitely spent some cycles considering how to addresss this before deciding to trust that it wouldn't happen.

Got tripped up briefly not clearing the `disallowed` set in part 2, not a huge problem.
Otherwise, smooth solve.
