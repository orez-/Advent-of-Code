# Day 12: The N-Body Problem

## Problem Summary ([?](https://adventofcode.com/2019/day/12))

The problem input contains the three-dimensional coordinates of four moons.
They start with no velocity, but each tick we update the velocity based on custom gravity rules, and the positions based on velocity (in that order).
Gravity is axis-independent, and only shifts the velocity by exactly -1, 0, or 1 between each moon, depending on their relative positions.
eg, if Europa is at 0, 2, 8 and Callisto is at 2, 2, 2, Europa's velocity is modified by 1, 0, -1 and Callisto's is modified by -1, 0, 1.

**Part 1** asks for the total "energy" in the system.
It defines potential energy of a moon as the Manhattan magnitude of its position from the origin, and its kinetic energy as the Manhattan magnitude of its velocity, and asks us to multiply these together for each moon and sum them for the solution.
The answer for my input was 7202.

**Part 2** asks for the time at which the moons return to their initial state.
The problem notes that the naive solution will not be efficient enough to produce an answer
The answer for my input was 537881600740876.


## Retrospective

Real life kicked my ass on this one.
I was dead-tired going into it, not nearly enough sleep.

I managed to produce some grotesque code for part 1, nowhere near placing.
For part 2 though I never did end up figuring out the trick.
I ended up looking up a hint after the fact that gave it away.
The key is that unlike real gravity, the gravity that's defined here is axis-independent.
This means we can search for the period of each axis independently, then find the least common multiple of all three for the answer.

Looking for improvements to my process here, the easy win seems like "get more sleep, nerd".
Although part of what's been eating my sleep time **is** Advent of Code.
So I guess the takeaway is "move to the west coast" 🤷‍♀️.
