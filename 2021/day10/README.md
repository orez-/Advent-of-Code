# Day 10: Syntax Scoring

**Language: [Jelly](https://github.com/DennisMitchell/jellylanguage)**

## Usage

Installation instructions for Jelly can be found at https://github.com/DennisMitchell/jellylanguage

```bash
jelly fun part1.jelly
jelly fun part2.jelly
```

The interpreter is also available online: https://tio.run/#jelly

## Problem Summary ([?](https://adventofcode.com/2021/day/10))

The problem input contains lines composed of opening and closing characters: `()`, `[]`, `{}`, and `<>`.
A correct line would always close the innermost opening character and end with all opening characters matched with a closing character.
Unfortunately, we're told we have no correct lines.
Instead, all of our lines are either **corrupted** or **incomplete**.
- A **corrupted** line tries to close with a character that does not match the innermost opening character.
- An **incomplete** line matches correctly, but does not close all opening characters.

**Part 1** asks us to find all the corrupted lines, and find the first unmatched closing character for each.
Each type of character grants some number of points: 3 for `)`, 57 for `]`, 1197 for `}`, and 25137 for `>`.
We're asked to sum the points for each corrupted line.
The answer for my input is 388713.

**Part 2** asks us to discard the corrupted lines, and instead find the shortest string that would complete each incomplete line.
We can score such a string: 1 for a `)`, 2 for a `]`, 3 for a `}`, and 4 for a `>`.
However, as we move along the string we multiply the running score by 5 while summing.
eg, `])}>` would total 294: `(2 * 125) + (1 * 25) + (3 * 5) + (4 * 1)`.

We're not done there though: once we have all the scores, our answer is their median.
The answer for my input is 3539961434.

## Solution

You can see the breakdown explanation of my solution [here](how_it_works.md).

## Retrospective

Hoo-whee.
I've seen Jelly around the [Code Golf Stack Exchange](https://codegolf.stackexchange.com), but I've never tried it before.
I figured it couldn't be so much harder to learn than any other esolang I've tried.
After all, it's meant to actually be useful!
Sure it uses funny unicode characters, but after you learn what those map to, how bad could it be?

Here's a few of the ways my thinking here was wrong:
- I have never worked in such a brutally [tacit programming style](https://en.wikipedia.org/wiki/Tacit_programming) before.
  In Jelly you get expressions (which can accept up to 2 arguments, infix), functions (contained entirely within a line, and referred to by their line number[^lineno]), and one (1) register.
  That's it.
  You can store whatever state you want in a list in that register, of course, but Jelly's functions don't flow nearly as nicely like this!
- It turns out that encoding as much functionality as possible in a byte means you gotta learn a lot of bytes to get ramped up.
  Combine that with a handful of modifier bytes which can arbitrarily change the meaning of a command, AND the fact that commands can mean different things if they're called as [a nilad, monad, or dyad](https://github.com/DennisMitchell/jellylanguage/wiki/Tutorial#1tacit-programming), or if they're called against a list vs an int.. there's a lot to learn!
- And a lot which can go wrong in confusing ways!
  Since Jelly is a golfing language, everything is geared around minimizing source code length.
  This means code will try to take meaningful action given ambiguous inputs, and outputs will often be in condensed formats, rather than more longform (more debuggable) formats.
  There aren't even any comments to temporarily comment out code!

I think the canonical way to solve part 1 would be to maintain a stack of the opening characters you've seen, and pop off the top of the stack as you find their matching characters.
If you pop a char that doesn't match, you've found a corrupted line.
I spent a bunch of time trying to figure out how to maintain state like this (or even allow it to flow through the code with some other data), but I eventually realized I might need to think outside of performance-minded solutions.
Instead, I take each input line and remove all occurences of well-formed unit chunks (`()`, `[]`, `{}`, and `<>`) on loop until there's no more to remove.
The first remaining closing character is the one we use for scoring.

Once we have this process, part 2's algorithm is pretty straightforward.
Discard condensed lines that contain a closing character, and we're left with the unmatched opening characters for the incomplete lines.

One quick note on my code.
Jelly is designed with small programming challenges in mind, and has a bunch of nice options for accepting input.
That said, I wasn't able to find a way to read all lines from a file: the function to read a full line panics on EOF.
I ended up hardcoding the number of lines in the file into my solutions to get around this.

I've always been impressed with Jelly's ability to express solutions to coding challenges so succinctly, but after using it I have a new respect for both the folks who use it and the folks who built it.
It's clear a lot of intention has been put into the language to cover a wide variety of common problems, and there's a whole lot of depth here to learn how to use the language well.
I'm almost certain there's more tricks to golf a few more bytes out of my solutions here, but this is all I've got for now!

[^lineno]: or position relative to the current function
