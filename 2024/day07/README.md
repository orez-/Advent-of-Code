# Day 7: Bridge Repair

## Usage

```bash
cargo run --bin day07 part1 < input.txt
cargo run --bin day07 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/7))

The problem input contains a list of mathematical equations missing their operators.
We're asked to find the equations which are solvable and sum their target values.

In **part 1** each missing operator is either addition or multiplication.
The answer for my input is 14711933466277.

In **part 2** the missing operator may also be concatenation.
The answer for my input is 286580387663654.

## Retrospective

I decided in part 1 to model each operator as a bit, and therefore each distribution of operators as a number.
I knew this wouldn't scale well in part 2, but it seemed like the least-effort way to iterate the options.
Sure enough: this went relatively smoothly, and part 2 added an additional operator.
Spent some time considering `itertools` options before settling on the recursive solution.
I tend to not like recursive solutions, which I picked up from working in Python for so long: in Python function calls have such a high performance impact it often makes a recursive solution more trouble than it's worth.
Even in Rust you risk hitting the recursion depth limit.
Looking at the input though, none of our equations have more than like 10 terms, so this wasn't worth worrying about.
Finding the product of operators recursively works well: well enough that I went back and retrofitted my part 1 solution with this approach.

Spent a little time debugging concatenating in the wrong order, since I decided to perform the concatenation mathematically instead of converting to and from strings.
Otherwise, relatively smooth solve.
