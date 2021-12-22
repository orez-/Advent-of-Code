# Day 17: Trick Shot

**Language: [Quorum](https://quorumlanguage.com/)**

## Usage

Installation instructions for Quorum can be found at https://quorumlanguage.com/download.html , but since it doesn't(?) support Linux I ended up using the interpreter on the [main page](https://quorumlanguage.com/).
All inputs are hardcoded in my solution.

## Problem Summary ([?](https://adventofcode.com/2021/day/17))

In this problem we fire a probe in a 2D plane, with an arbitrary (integer) initial x and y velocity.
The probe moves in discrete steps via some simple rules:
- the x velocity is added to x
- the y velocity is added to y
- the x velocity is dampened by 1
- the y velocity drops by 1

The problem input describes a small axis-aligned rectangle we're trying to hit.
The rectangle is only consider hit if the probe is within the rectangle after a step.
The probe moving through the rectangle mid-step does not count.

**Part 1** asks for the maximum height of the highest possible shot that still hits the rectangle.
The answer for my input is 4851.

**Part 2** asks for the count of all possible initial x and y velocity combinations.
The answer for my input is 1739.

## Retrospective

It turns out there aren't a lot of languages that start with the letter Q, and most of those that do deal with [quantum computing](https://en.wikipedia.org/wiki/Quantum_programming).
Quorum claims to be an "evidence-oriented" programming language, which is to say their design decisions are based on usability and teachability research.
I'm a little skeptical of their results.
I'm all for re-examining traditional design decisions and trying new things, but Quorum feels more like a few new keywords layered over an old version of Java.
I didn't have to wrestle with the language so much (once I gave up on installing it locally), but it definitely felt more like a Groovy than a Nim.

Today's problem was pretty fun!
I wouldn't've assumed there was a max height if the problem hadn't asked for one.
For part 2 I tried calculating the times a given y coordinate would hit the square, then finding all the x coordinates that would hit at those times.
I tried solving this mathematically, without loops, and I believe I eventually did so, but failed to account for shots which hit the loop multiple times, meaning I was double-counting some cells.
I got around this issue by enumerating the cells in a loop, thus eliminating any cool performance improvements.
Oh well!
