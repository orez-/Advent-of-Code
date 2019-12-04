# Day 4: Secure Container

## Problem Summary ([?](https://adventofcode.com/2019/day/4))

This puzzle has us identifying numbers in the given range (367479-893698 for me) where two adjacent digits are the same and the digits never decrease left to right, only increase or stay the same.

For **part 1** the answer is the count of all such numbers.
The answer for my input is 495.

**Part 2** is the same, but with the additional constraint that the two adjacent digits only count in a group of exactly two.
The answer for my input is 305.


## Retrospective

Part 1 here was a regex checking for the double-adjacent, and a comparison against the sorted version of the digits for the never-decrease check.

The trick to part 2 is, since we're guaranteed the digits of matching numbers are never decreasing, the double-adjacent check can just be a total count of the digits without worrying about adjacency.
This means we can use `collections.Counter` to count up and identify our digit groups.
I'm glad this worked out, because I completely forgot about `itertools.groupby` until like an hour later.

I managed to put this together pretty quickly and place pretty well for both parts.
I appreciate that the problem description of this one was shorter than the previous days this year so far.
I've been missing important details trying to speed read.
Even on this one, for part 1 I submitted the first number I found that matched instead of reading that I needed to output the count.
I made an effort this time to make sure I read carefully (which paid off in part 2), but I guess I need to be even more careful.
