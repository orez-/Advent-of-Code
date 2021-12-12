# Day 12: Passage Pathing

**Language: [Lua](https://www.lua.org/)**

## Usage

Installation instructions for Lua can be found at https://www.lua.org/start.html

```bash
lua part1.lua < file.txt
lua part2.lua < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/12))

The problem input describes bidirectional connections between caves.
Starting from `start`, we want to explore some of the caves while making our way to the `end`.
We also make the distinction between big and small caves.
Big caves are denoted with capital letters and can be visited any number of times.
Small caves are denoted with lowercase letters, and have restrictions on how many times they can be visited.
We're tasked with finding the number of unique paths through the cave system.

In **part 1** each route is only allowed to visit each small cave at most once.
The answer for my input is 3510.

In **part 2** each route is additionally allowed to visit **one** small cave twice (not including `start` or `end`).
The answer for my input is 122880.

## Retrospective

Lua is one of the few languages this year I've used a fair bit before--not professionally, but for game jams!
I remember enjoying it, but it's been a few years since I used it last.
I'm glad to have another excuse to dip back into it.

I remembered Lua being a little weirdo, a little jank (in an endearing way), but I forgot some of the exact details here.
I remembered [tables](https://www.lua.org/pil/2.5.html) and the lack of arrays.
Something vaguely about metatables?
I still don't remember this.
The big thing I forgot was that there's no name errors: accessing an undefined field gives you `nil`.
This can be a tricky source of bugs: I had a `wrongField == constant` conditional that was always evaluating to false.
I'm not surprised I haven't seen more languages adopt this "feature".

Overall though, getting this DFS solution together was no problem in Lua (which is nice--I'm still recovering from the one-two punch of Idris and Jelly).
Despite its quirks, or even because of them, it's a fun language to hack something together in.
