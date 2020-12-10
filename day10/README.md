# Day 10: Adapter Array

## Problem Summary ([?](https://adventofcode.com/2020/day/10))

This puzzle's input describes a series of electronic adapters which can accept a certain "joltage".
An adapter with a rating of `x` can accept as input a joltage in the range `[x-3, x]`.
The wall outlet starts with a joltage of 0, and we're trying to charge a device whose joltage is three higher than the highest adapter.

**Part 1** asks us to use every adapter in the input, and count how many joltage jumps are 1 and how many are 3.
We're then asked to multiply those counts together.
The answer for my input is 2272.

**Part 2** asks how many different combinations of adapters there are to connect the outlet to the device.
The answer for my input is 84627647627264.


## Retrospective

I had a lot of trouble separating flavor text from the important information on this one, for whatever reason.
My brain kept snagging on the word "joltage".

For part 1 I sorted the list and counted the number of +1s and +3s _within the list_, which didn't include the initial jump from 0 or the final +3 jump to my device.
In solving this I didn't recognize this at all; I ran the example input and noticed my counts were one lower than theirs and tried just adding one to my counts(!).
This was right for the final jump, but the initial jump could've been a 1, 2, or 3, and I got lucky that my input had it as a 1 (or maybe the inputs were designed to accomodate yutzes like me).

Part 2's description made explicit that some [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) trickery was required.
I never quite have the knack for combinatorics problems like these, it's always a struggle for me to think through the math required.
The important observation is that the number of ways to reach a joltage `j` is equal to the sum of the ways to reach joltages `j-3`, `j-2`, and `j-1`
(the "recurrence" I think? It's been a while since I needed to do this formally!).
I don't think I recognized this in these exact words; looking at this now I'd probably have just kept a dict `ways = {joltage: ways_to_reach_this_joltage}` and populated it in-order by `ways[j] = ways.get(j - 1, 0) + ` etc.
I did have such a dict, but I also did some weird juggling act with a queue that's unnecessary in retrospect.

Thinking on it now, if space were a concern you'd only actually need to keep at most three joltages at a time.
But of course for Advent of Code we're optimizing for time to solve, not space.

We're starting to get into more tricky ones, in my opinion!
I liked this puzzle.
Puzzles where you're just translating the algorithm described in the problem text into code as fast as possible are fine, but I'm a big fan of ones where you have to come up with a more efficient solution.

Didn't place, but I'm pretty happy with how fast I got this one.
