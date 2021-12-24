# Day 20: Trench Map

**Language: [TypeScript](https://www.typescriptlang.org/)**

## Usage

Installation instructions for TypeScript can be found at https://stackoverflow.com/a/58689284/1163020

```bash
ts-node main.ts part1 < file.txt
ts-node main.ts part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/20))

The problem input defines a small portion of an infinite grid of lights, all otherwise off if not indicated.
It also defines how these lights decide to turn on or off.
Each step, each light turns on or off depending on the pattern of its 3x3 surrounding lights.

**Part 1** asks us how many lights are on after two steps.
The answer for my input is 5301.

**Part 2** asks us how many lights are on after fifty steps.
The answer for my input is 19492.

## Retrospective

Fun problem.
I assumed the challenge was meant to be in the infinite grid, which is easily solved by keeping the lights in a coordinate map instead of an array.
But instead we need to observe that the case when _no_ surrounding lights are on turns them on, and _all_ surrounding lights on turns them off.
This is why we always iterate by an even number: every other step there are an infinite number of lights on!
I submitted a couple incorrect counts before realizing my mistake here.
Fortunately modifying my solution to support this was easy.
I just had to replace my out-of-bounds coalesce with a 1 instead of a 0 every other call.

I've done a bit of TypeScript previously, professionally even.
I'm not the biggest fan of a lot of Javascript's decisions, and I don't believe trying to wedge explicit types into the system really helped anything.
Still, as such a popular language there's plenty of help available.

TypeScript gripes:
- Iterators don't have a `reduce` function, you need to convert them to an Array first.
  Yuck.
- It's so frustrating that js doesn't have a stdlib way to use a tuple-alike as a map key.
  The easiest way to handle this is _still_ to convert it to a string first.
  This is just so comically unacceptable for a modern, globally popular language.
