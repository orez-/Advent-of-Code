# Day 5: Binary Boarding

## Problem Summary ([?](https://adventofcode.com/2020/day/5))

The puzzle's input contains a list of seat ids for a flight.
The seat ids are in a format where each digit subdivides the space:
an F means the seat is in the front half while a B means the back half.
The next F or B subdivides that space, and so on.
Similar rules apply for the three digits of Left and Right.
The seat number can be derived by multiplying the row by 8 and adding the column.

**Part 1** asks for the highest seat number.
The answer for my input is 901.

**Part 2** asks us to find the single missing id that isn't at the front or back of the plane.
The answer for my input is 661.


## Retrospective

The Advent of Code site took a full minute to load for me!
At least one friend also had this issue.
Not great!

The key to doing this problem quickly was identifying that the ids are just the binary definition of the number.
Replace F and L with 0, B and R with 1.
I had a little trouble parsing what part 2 was asking at first, but for the solve I ended up printing all the missing numbers and hand-picking the one that wasn't in the front or back.
In retrospect just doing the +1/-1 check wouldn't have been that much slower, but I'm glad I didn't overcomplicate it.

Didn't place!
But within top 150 for both parts.
I wonder if I could've placed if the site had loaded, but it's tough to tell.
