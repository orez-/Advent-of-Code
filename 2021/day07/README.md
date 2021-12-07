# Day 7: The Treachery of Whales

**Language: [Groovy](http://groovy-lang.org/index.html)**

## Usage

Installation instructions for Groovy can be found at https://groovy.apache.org/download.html

```
groovy part1.groovy < file.txt
groovy part2.groovy < file.txt
```

I kept getting build warnings that ["An illegal reflective access operation has occurred"](https://stackoverflow.com/q/47935772/1163020).
I don't think it's an issue with my code, and it doesn't seem to affect the output, so I didn't bother sorting out how to suppress it.

## Problem Summary ([?](https://adventofcode.com/2021/day/7))

We're given a list of integer values, each representing a location.
We're told we need to increment or decrement each of the values a step at a time to align them all on the same integer value.
There is a cost associated with moving a value, and we want to minimize and calculate the cost.

In **part 1** moving a number one step costs 1.
The answer for my input is 344735.

In **part 2** moving a number by one step costs one more than its last move did.
That is, the first step costs 1, the second step costs 2, the third step costs 3, and so on.
The answer for my input is 96798233.

## Retrospective

This is the first language this year that I've worked with professionally, in the form of Jenkins scripts.
My previous experiences didn't exactly leave me eager to return to Groovy, but honestly my original plan for today fell through[.](https://github.com/fgmccabe/go/blob/master/InstallingGo.rtf)
Moving right along!

I took a minute for part 1 to consider an efficient way to find the answer.
I like what I came up with:
- Consider the smallest value (call it `a`) and largest value (`z`).
  We know that the alignment point must lie between them, and in fact any point between them (`p`) will have the same total cost in terms of them:

  ```
  cost = (z - p) + (p - a)
  cost = z - a
  ```
- We can then look at the next smallest value and next largest value.
  We know that any alignment point between them will have the same (minimal) cost, and will be a legal minimal alignment point for the original `a` and `z`.
- We can repeat this process until we've consumed all elements, and return the total.
  The runtime complexity here is O(nlogn) to account for the sorting step, where n is the number of values (so, 1000).

Part 2 is a little trickier.
I spent a little time looking for insight for a similarly quick solution.
I think you could probably do something clever with dynamic programming here, but instead of any of that I just brute forced it: try every pivot point between `a` and `z` and take the minimum.
O(nm), where m is the distance between `a` and `z`.
Not great, but gets the job done.
I'm curious to look into what other folks have done here[^1].

I haven't really used any of the functional features of Groovy or even Java before.
They're.. something!
I ran into a lot of silly type errors, and got bitten by associativity when omitting parens a few times.
I'm still not eager to spend more time with Groovy, but overall you could definitely do worse.

[^1]: Since writing this I've been directed to https://www.reddit.com/r/adventofcode/comments/rawxad/2021_day_7_part_2_i_wrote_a_paper_on_todays/ , which proves that the answer is within 0.5 of the average of all the values.
