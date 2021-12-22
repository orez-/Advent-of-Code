# Day 18: Snailfish

**Language: [Rust](https://www.rust-lang.org/)**

## Usage

Installation instructions for Rust can be found at https://www.rust-lang.org/learn/get-started

```bash
rustc main.rs
./main part1 < file.txt
./main part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/18))

This problem describes "snail numbers".
A snail number is either a regular number, or a pair of snail numbers `[x,y]`.
We define the addition of two snail numbers `a` and `b` as combining them into a pair, `[a,b]`, but note that they must be in **reduced** form.
To reduce a snail number, we apply the following rules in order from left to right until none apply:
- If any pair is nested four or deeper we `explode` that pair, replacing it with 0 and adding the left.
- If any regular number `x` is larger than 10, we `split` it, by replacing it with a pair `[⌊x/2⌋, ⌈x/2⌉]`.

We also define the **magnitude** of a snail number, which is 3 times the magnitude of its left element plus 2 times the magnitude of its right element.
The magnitude of a regular number is just that number.

**Part 1** asks for the magnitude after summing together all of the snail numbers in our list in order.
The answer for my input is 3647.

**Part 2** asks for the largest magnitude possible from summing two snail numbers from our list, noting that snail number addition is not commutative.
The answer for my input is 4600.

## Retrospective

Finally, Rust!
Today's my "cheat day" this month.
While I have little to no practice with most of the languages on this list, Rust is a strong contender for my most-used language this year.
I'm a big fan.

Today's challenge was all about the fiddly implementation details, which is fine by me.
Rust isn't the easiest tool for working with tree structures like this, but it's a great tool for
fiddly implementation details.
The `explode` operation acting on the "left" and "right" values suggests it would be good to keep each snail number as a flat list, but all the other operations have to deal with depth.
Tracking both a flat list and a tree might have helped, but this approach seemed computationally tough to maintain.
Ended up going with just a tree structure after all, and getting a little tricky with `explode`.

For `explode` we recursively walk the tree left to right, then when we find a too-deep pair we zero it out and send back that original pair.
As the `explode` methods return back through the call stack, we can then issue no more than one request to add `left` to the pair's left's rightmost leaf, and no more than one request to add `right` to the pair's right's leftmost leaf.

Final thoughts:
- Working through this today I ran into a couple issues that might have frustrated me in a different language, but my familiarity with Rust helped me debug more quickly.
  I think this is a good reminder how effective practice is at dulling these pain points.
- My solution today was a lot of code, more than I think another language might have used.
  That said, once I got the basics down the solution came together without much issue.
