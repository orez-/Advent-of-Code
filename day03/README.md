# Day 3: Crossed Wires

## Problem Summary ([?](https://adventofcode.com/2019/day/3))

Input file contains two lines, with the definition for the shape of a wire (path) on each line.
Wires are defined by comma-separated segments.
Each segment is a direction (Up/Right/Down/Left) and a distance.
These two wires end up intersecting each other at multiple points.

**Part 1** of this question asks to find the Manhattan distance of the intersection point nearest the origin.
The answer for my input is 529.

**Part 2** of this question asks to find an intersection point minimizing the sum of the distances along each wire, and the result of that sum.
The answer for my input is 20386.


## Retrospective

I got tripped up trying to come up with a nice solution for calculating intersections, when just enumerating all the spots on the wire would've been much faster and easier to debug.
In fact, I ended up having trouble debugging the nice solution for part 2, and ended up rewriting it enumerating all the spots anyway.
Every year I need a reminder to not spend a lot of time on a clever solution, and I'm hoping this is enough of a reminder.

Using `range` objects to check if an integer falls in a range is really nice.
