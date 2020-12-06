# Day 6: Custom Customs

## Problem Summary ([?](https://adventofcode.com/2020/day/6))

Each unique character in the puzzle input describes a different question asked to a person.
Each line in the input describes the questions answered by a single person.
Different groups of people are delimited by a blank line.

**Part 1** asks how many unique questions were asked in each group (not necessarily unique across groups).
The answer for my input is 6911.

**Part 2** asks how many questions were asked to each person within a group.
The answer for my input is 3473.


## Retrospective

I had a lot of trouble grokking the file format!
Lost a bunch of time just reading and rereading the puzzle definition.
I'm still not sure I totally understand what it's trying to convey in-lore.

After I understood the format part 1 came together quickly, but I missed placing by a lot.
But, I recognized that part 2 was asking for set intersection instead of set union quickly, and was able to put the solution together quickly.
Placed 84th!
Not fantastic but I'll take it at this point.
Competition's getting tough.

It looks like I'm going to want to make a helper function to parse out groups from the input.
