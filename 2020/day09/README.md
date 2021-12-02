# Day 9: Encoding Error

## Problem Summary ([?](https://adventofcode.com/2020/day/9))

This problem describes a checksum algorithm for the input, whereby every number must be the sum of two of the numbers in the 25 lines prior.
The first 25 lines are exempt from this.

**Part 1** asks us to find the number that does not pass this checksum.
The answer for my input is 26134589.

**Part 2** asks us to find a contiguous set of at least two numbers that add up to the answer to part 1.
We are to sum and output the smallest and largest values in this range.
The answer for my input is 3535124.


## Retrospective

I was exhausted going into this one.

I messed up the check in part 1.
The code I wrote required each number in the running total to have a match summing to the value, which obviously didn't happen.

I forgot the param name for `maxlen` on queues.
I miss working in python.

I got tripped up over int-ing the list for a bit.

Part 2 came together nicely though.
Starting with the goal value, we subtract each number in order until we dip below zero, then we add them back on from the front.
When we hit 0 we know we have our answer.
I like this O(n) solution, but looking at other folks's answers I probably would've been fine with the faster-to-implement O(n²) solution.

I didn't think to write a check to ensure I didn't just return the value itself, but it didn't end up being a problem.

Didn't place.
