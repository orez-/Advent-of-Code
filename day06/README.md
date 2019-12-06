# Day 6: Universal Orbit Map

## Problem Summary ([?](https://adventofcode.com/2019/day/6))

The input file contains the edges of a directed graph.

**Part 1** asks how many paths total there are between nodes.
This includes paths that traverse multiple edges, but not 0-length paths.
The answer for my input is 322508.

**Part 2** removes the directed constraint, and asks the distance between two specific nodes.
The answer for my input is 496.


## Retrospective

Heck yeah, graph traversal!

Today went really well for me.
Placed pretty highly.
For whatever reason I have a lot of practice throwing together BFS + DFS in python, so the only tricky part was reading carefully and making sure I was actually solving the problem as stated.

If I were building this to spec I'd have to check what SAN and YOU were orbiting before doing the distance calculation for part 2.
Since the goal is to get the answer as fast as possible though I just grepped the file for the orbits and hardcoded em.
Definitely the right move.

I wonder if we're going to have to make use of this file format in a future problem.
