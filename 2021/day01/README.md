# Day 1: Sonar Sweep

**Language: [AWK](https://en.wikipedia.org/wiki/AWK)**

## Usage

Most UNIX-y systems should provide an `awk` command.

```bash
cat file.txt | awk -f part1.awk
cat file.txt | awk -f part2.awk
```

## Problem Summary ([?](https://adventofcode.com/2021/day/1))

**Part 1** gives us a list of numbers, and asks how many consecutive numbers are increasing.
The answer for my input is 1722.

**Part 2** asks us to compare overlapping windows of three numbers, and asks how many consecutive windows have increasing sums.
The answer for my input is 1748.


## Retrospective

I've only played with AWK a very little bit previously.
I usually default to a more powerful scripting language for the type of problem AWK really shines at.
However I quite like writing AWK; the syntax is able to be very simple, and I'm always surprised with how featureful it actually is.

My solution to part 1 runs only two patterns over each line in the file: one to increment a counter when the current line is greater than a variable `lastLine`, and an unconditional command to update `lastLine`.
One issue that tripped me up was `lastLine`'s default value (0?) is considered lower than the first line, so my initial solution was off by one.
I initialize `lastLine` to a large value to avoid this issue.

Part 2 is worded as comparing 3-windows, but since we're just summing the windows the common two digits cancel and leave us comparing each line to the line three ahead of it, instead of the line one ahead of it.
Unfortunately my solution for part 1 isn't so easily modifiable to support lines + 3; I could have done some juggling to track the last three lines, sliding them down as we iterate, but this was starting to feel painfully unidiomatic.
Instead I decided to track each line of the file in an array, and increment the total where the current line is greater than `lineno - 3` from that array.
I still had to account for the issue mentioned above where the first couple lines counted as higher than the default value.
I ended up just subtracting 3 from the total for this.
This is technically incorrect for files of less than three elements, but the input file has more than three elements, so this isn't a problem.

There's probably a more scalable solution here: we really only need to keep the last three lines in memory, not the entire file.
In Advent of Code though, scalability is _not_ the name of the game.
These solutions got me the answer, and that's good enough!

This was a good warmup puzzle!
I love a good puzzle that expresses a requirement, but allows for insight to simplify the definition, and this was a perfect little example of that.
