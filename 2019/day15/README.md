# Day 15: Oxygen System

## Problem Summary ([?](https://adventofcode.com/2019/day/15))

A robot with an [Intcode](../day09) brain is in a grid made of walls, open area, and one square containing an oxygen system.
We don't know the layout of the grid, but we can command the robot to move in the four cardinal directions and it will respond with whether it hit a wall and can't move, moved into an open area, or moved to the oxygen system.

**Part 1** asks for the fewest number of steps to walk to the oxygen system.
The answer for my input is 304.

**Part 2** asks how far the oxygen system is from the open area farthest from it in walking distance.
The answer for my input is 310.


## Retrospective

This problem was a great exercise in breadth first search.
I wrote three separate variants on breadth first search for this problem.
My solution does a BFS to decide where the robot should move next to explore, preferring the shortest route to unexplored areas.
Once we've explored everywhere we do a BFS to find the walking distance between the origin and the oxygen system.
And then in part 2 instead of finding distance between points we do a BFS over the whole area to determine the farthest distance.

Besides a few typos no big problems with getting the solution for this one together.
Fun one!
Decent placement on both parts.

I think there might've been the possibility that the bot couldn't decide which way to go while mapping the area, would get stuck in an indecisive loop.
So uhhhh good thing that didn't happen!!
Maybe since I always explore in the same order each time this wasn't a possibility.
