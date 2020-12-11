# Day 11: Seating System

## Problem Summary ([?](https://adventofcode.com/2020/day/11))

The problem input describes a field of floor and empty seats.
The puzzle describes the conditions by which seats become occupied or unoccupied based on surrounding seats.
We're tasked with finding the count of occupied seats once the field is stable and no seats change state.

In **part 1** a seat will become unoccupied when at least four of the eight immediately adjacent tiles are occupied.
A seat will become occupied if none of the immediately adjacent seats are occupied.
The answer for my input is 2283.

**Part 2** changes the rules so the count is based on the first visible chair in the eight cardinal directions.
When at least five occupied chairs are visible from an occupied seat it will be vacated,
and when no occupied seats are visible from an empty seat it will become occupied.
The answer for my input is 2054.


## Retrospective

Cellular automata problem.
Nothing too special in the solve.
In part 1 I got the sense that having a separate function to check adjacency would be helpful, and it turns out it was *very* helpful!
Part 2's main function is almost identical to part 1's, just with a different adjacency function, which made the solve go smoothly.

I felt a little bit sluggish in the solve, but I placed in the 30s for both parts.
Happy with this.
