# Day 23: Amphipod

**Language: [Wren](https://wren.io/)**

## Usage

Installation instructions for Wren can be found at https://wren.io/getting-started.html

```bash
wren_cli main.wren part1
wren_cli main.wren part2
```

Part 2 takes \~30 seconds to run on my machine.

## Problem Summary ([?](https://adventofcode.com/2021/day/23))

The problem input describes a 2D grid with a hall and four rooms.
Eight pieces need to be moved into the rooms: two 'A's in the first room, two 'B's in the second,
two 'C's in the third, and two 'D's in the fourth.
The pieces cannot move past each other, and can only be moved twice max: once into the hall, and/or once into the proper room.
Each move has a cost associated with it too: each step an 'A' takes costs 1, 'B' costs 10, 'C' costs 100, and 'D' costs 1000.
We're tasked with finding the cheapest cost to get all the pieces to their correct rooms.

The answer for **part 1** for my input is 15516.

**Part 2** adds eight more pieces to the input.
The answer for my input is 45272.

## Retrospective

I don't think I've talked about this previously, but I like the setup in Advent of Code where you don't know what part 2 will ask until you finish part 1.
There's an element of predicting how you'll have to modify your part 1 code, and writing it such that such a change won't be more effort than necessary.
I'm not sure what I was predicting for this one, but I definitely missed the mark.
I originally special-cased the two rows for the rooms, which did not scale very well when adding two more rows.

For part 1 I tried for a best first search first, but it solved too slowly.
Modified it into an A\*, with the heuristic cost as the total of the distance from each out-of-position piece to the top of its room.
The priority queue implementation I [found on Rosetta Code](https://rosettacode.org/wiki/Category_talk:Wren-queue) for this was passable, but slow under any sort of load.
Part 1 took 17 seconds to run, there was no way part 2 was going to work.
I ended up having to write [my own](queue.wren) priority queue, based on [Python's](https://github.com/python/cpython/blob/main/Lib/heapq.py).

I learned about Wren just over a year ago.
It's one of the languages that motivated me to do this challenge, to have an excuse to try it out.
The stdlib seems a bit light (though not nearly as light as Virgil), but overall I like it.
Feels a lot like a streamlined, stripped down Ruby.

I ended up having to update my OS Release for the right libc version dependency.
This was a pain in the ass, but I'm glad I got a chance to try Wren.

Wren thoughts:
- Fibers are cool.
  I only really used them like a Python generator but it looks like they've got a bunch of concurrency utility.
- Maps can only keep primitives.
  I ended up using the board state's `toString` as map keys, which I can't imagine helps my runtime.
- Lists do equality by identity.
  This is a real shame.
- Ranges automatically stepping up or down appropriately is really nice, and very helpful in my solve.
