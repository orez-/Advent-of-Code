# Day 16: Flawed Frequency Transmission

## Problem Summary ([?](https://adventofcode.com/2019/day/16))

This problem defines a method to transform the digits of an input list based on a repeating pattern digit list (`0, 1, 0, -1`).
Each digit becomes the ones digit of the sum of the digits in the input, each multiplied by the digits in the _extended_ pattern.
The pattern is extended by repeating each digit by the index of the digit in the input (1-indexed).
We also skip the first element of the pattern.

**Part 1** asks us for the first eight digits of the result of running this transformation 100 times on the input.
The answer for my input is 77038830.

**Part 2** takes the first seven digits of the input as the message offset, and also repeats the input signal 10,000 times.
It asks for eight digits starting at the offset, of the result of running this transformation 100 times.
The answer for my input is 28135104.

The problem statement for today is particularly convoluted, and my summary of it is probably unclear.
For more details definitely check out the [actual problem definition](https://adventofcode.com/2019/day/16).


## Retrospective

For part 1 I spent a lot of time crafting my initial implementation and making sure it was correct.
Lotta fiddly details to get wrong.
Made it low on the leaderboard, no regrets.

Part 2 was a critical thinking one, had to really understand the properties of the problem instead of just understanding the steps to implement in isolation.
The two key observations that made this problem solvable were that my seven-digit offset was greater than half the signal length, and the pattern was `0, 1, 0, -1`.
This meant a few things:
- the digits from `offset` onward can be calculated only by summing all digits including and following it (pattern of `[0] * (offset - 1) + [1] * offset`)
- we _never_ need to calculate the first `offset` digits, since they don't factor into the final output
- we can perform a rolling sum when calculating digits to save some time

Ended up placing pretty well for part 2, especially considering how much time I spent staring at it thinking "please just let this be an implementation problem, don't make me have to understand these properties I've slapped together".

This is definitely a cool problem, but I'm **very** much not a fan of it for Advent of Code.
Implementing a long series of arbitrary and easy-to-mess-up rules for number transformation kind of sucks, and then having to understand those arbitrary rules to infer other properties is just not the kind of problem I want to solve for a timed midnight challenge.

In past years I've learned that pypy can be considerably faster than CPython for pure python programs such as the ones I write for Advent of Code.
My solution for today's problem was a good example of this: my solution for both parts runs in four seconds under pypy but fifteen with CPython.
