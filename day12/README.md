# Day 12: Rain Risk

## Problem Summary ([?](https://adventofcode.com/2020/day/12))

The problem description describes controls for a ferry.
Each command is a character representing an action, and a number.
We're tasked with finding the Manhattan distance from where the ferry starts to where it ends up.

In **part 1**:
- Action N means to move north by the given value.
- Action S means to move south by the given value.
- Action E means to move east by the given value.
- Action W means to move west by the given value.
- Action L means to turn left the given number of degrees.
- Action R means to turn right the given number of degrees.
- Action F means to move forward by the given value in the direction the ship is currently facing.
The ferry starts facing east.
The answer for my input is 1645.

**Part 2** defines a "waypoint", which exists relative to the ferry and starts at 10, -1.
- Action N means to move the waypoint north by the given value.
- Action S means to move the waypoint south by the given value.
- Action E means to move the waypoint east by the given value.
- Action W means to move the waypoint west by the given value.
- Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
- Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
- Action F means to move forward to the waypoint a number of times equal to the given value.
The answer for my input is 35292.


## Retrospective

Not a whole lot to say about this one.
Felt like a pretty straightforward implementation problem.
I think the important implementation decision in part 1 was how to express the direction the boat was facing.
I went for rotating a unit vector, which meant my rotation for part 2 was almost identical to part 1.

I placed pretty well in part 1, and top 10 in part 2!
Very happy with this.
