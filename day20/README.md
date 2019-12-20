# Day 20: Donut Maze

## Problem Summary ([?](https://adventofcode.com/2019/day/20))

The input describes a maze with teleporters around the edges.
The goal of the maze is to get from label AA to ZZ in as few steps as possible.
Taking a teleporter takes one step.

**Part 1** asks for the number of steps in the minimum solution.
The answer for my input is 620.

**Part 2** adds that going through a teleporter on the inside of the ring takes you down a layer, and from the outside of the ring takes you up a layer.
The entrance and exit are the only paths on the outermost layer, and only exist on the outermost layer.
We're again tasked with finding the number of steps in the minimum solution.
The answer for my input is 7366.


## Retrospective

I made a bunch of mistakes today!

On part 1:

- Parsing the letters was kind of a pain.
  Neat little mini challenge, but I did not excel at it.
  - I noticed the teleporter labels were unique regardless of permutation, so I kept the labels as a `frozenset`.
    In retrospect I should've just gone for `''.join(sorted(label))`, much less confusing.
- Lost time for `.strip()`ping my input file.
  Turns out those leading spaces are crucial for alignment!
  Changed this to `.rstrip("\n")`, here and in my template file.
- Lost some time because the input isn't square!
  This year I've started defining bounds checks as `range` objects, so:

  ```python
  height = range(len(file))
  width = range(len(file[0]))
  print(x in width and y in height)
  ```

  Problem is the lines are all uneven lengths today!
  Ended up generating the width object on the fly for each row.

After all this, after parsing the board and teleporters, the BFS search came together no problem.

On part 2:

- I tried keeping a `best` dict, to track the shallowest depth at which we hit each point, to avoid repeating that point from a deeper depth.
  Turns out, not a valid optimization!
  Consider the case where we want to use the same teleporter many times to build up depth, before spending them all making a break for the exit.
  This "optimization" made my solution report the maze unsolvable.
- After a while of debugging I realized I had swapped my depth deltas: the outer ones were going deeper and the inner ones were going shallower.
  I swapped these, and then after a long period of debugging later realized I had had it right in the first place all along.
  Rough life.
- I swapped `steps` and `depth` when adding to the BFS queue in the teleport logic.
  This was bad.

In the end it turned out I didn't need any fancy optimizations for this.
It was really just a question of passing the depth in the BFS queue, and not botching the implementation.
Unfortunately I failed pretty hard in that regard.
Didn't place today, took too long.

I'm losing a bunch of time each day rewriting BFS and `[(0, -1), (0, 1), (1, 0), (-1, 0)]` and:
```python
    for y, row in enumerate(file):
        for x, elem in enumerate(row):

```
I should really build out some of these common operations in my starting template file.
