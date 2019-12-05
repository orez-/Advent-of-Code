# Day 1: The Tyranny of the Rocket Equation

## Problem Summary ([?](https://adventofcode.com/2019/day/1))

This problem defines a calculation for the fuel required to launch a given mass: `(mass // 3) - 2`
You are given a list of positive integer masses.

**Part 1** asks that we calculate the fuel needed for each mass in the list, and sum them.
The answer for my input is 3348430.

**Part 2** requires that we _also_ calculate the fuel needed to launch the fuel, and the fuel needed to launch _that_ fuel, and so on.
The answer for my input is 5019767.


## Retrospective

Not much to say here.
As in previous years, this was a good practice ramp-up problem for the rest of the month.
I spent more brain cycles than I should've trying to decide if I was supposed to sum then calculate or calculate then sum.
Really it should've been clear to me that it was calculate then sum; the sum is just to get a single value to submit, and having the subproblem of summing a file of integers is really uninteresting.

First day of the year is always busy.
I ended up picking up a few points on part 2, just missed for part 1.
