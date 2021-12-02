# Day 7: Handy Haversacks

## Problem Summary ([?](https://adventofcode.com/2020/day/7))

This puzzle deals with bags of different colors within other bags, the bags within those bags, and so on.
The input describes how many bags are directly contained within each color of bag.

**Part 1** asks how many different color bags contain your shiny gold bag, including indirectly.
The answer for my input is 332.

**Part 2** asks how many bags total are contained within your shiny gold bag.
The answer for my input is 10875.


## Retrospective

Part 1's challenge is in parsing the file into a data structure that we can [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) over.
I haven't been writing much Python this year, and I completely forgot how to extract the full-string match from a regex!
Had a little trouble deciding which direction the mapping had to go (inner -> outer), but I was able to barely place.

Part 2 I switched my algorithm to a recursive [DFS](https://en.wikipedia.org/wiki/Depth-first_search) instead, in anticipation of having to cache results for performance issues.
Some line in the problem description made me think this might be an issue, but in practice there aren't enough entries for it to be an issue.
I probably should've just modified my BFS from part 1.
I also had to spend some time fixing up my parsing code to read "leaf" bags correctly (bags containing no bags).
I did notice this would be an issue before I actually ran into it, so that's nice at least.
Didn't place on this part.

I'm excited to be getting into the graph search part of the year!
