# Day 13: Shuttle Search

## Problem Summary ([?](https://adventofcode.com/2020/day/13))

The problem input describes a bunch of buses.
Specifically, how often each bus leaves for the airport.
There are also a bunch of `x`s, representing buses we don't care about.
The buses all leave the station at time 0.

The input file also contains a number representing the time you arrive at the station. **Part 1** asks how long you'll have to wait for a bus, multiplied by its period. The answer for my input is 4315.

**Part 2** asks you to find the time `t` such that the first bus departs at `t`, the next bus departs at `t+1`, the next at `t+2` and so on.
Buses marked `x` are only used as offsets, and provide no additional constraints.
The puzzle warns that the solution is going to be huge, and indeed the answer for my input is 556100168221141.


## Retrospective

Ah yes, the [yearly modular arithmetic question](https://github.com/orez-/Advent-of-Code-2019/tree/master/day22).

To try to save a little time in part 1 I pulled the leading value out of the file and hardcoded it.
This ended up not actually saving a lot of time ᖍ(ツ)ᖌ.
I think there's a way to do this in `O(|buses|)` using some tricky modulo math, but in the interest of keeping it simple I just started trying values until I found one.
This worked!
Moving on.

For part 2 I'm almost certain that probably like Fermat has a formula that just solves this super easily.
I don't know anything about the properties of modular arithmetic though, so I just winged it.
I noticed that the first two buses (41,0 and 37,35) met our constraints at 779 and then met them again at 2296.
These two solutions have a difference of 1517, the least common multiple of 41 and 37.
Since the problem's solution must also meet these constraints, it _also_ must be of the form `t * 1517 + 779`, so I tried checking for the next bus for all whole-number values of `t` and incorporating _that_ solution into a new equation, and so on until all buses were accounted for.
And this totally worked!
My program runs in 325 iterations, WAY faster than the naive 556100168221141 iterations.

This was a cool problem!
I don't love that I just had absolutely no chance for the leaderboard today, but I'm really happy I was able to piece this one together without any hints.

Also, I'm a huge fan of word problems of the form "foo is trying to solve a word problem and needs your help".
