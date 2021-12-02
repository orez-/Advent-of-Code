# Day 2: Dive!

**Language: [Befunge-93](https://esolangs.org/wiki/Befunge)**

## Usage

I didn't find a satisfying answer for a good, canonical Befunge interpreter for a Unix system.
I ended up using an online interpreter to test my work.

http://www.quirkster.com/iano/js/befunge.html

If you decide to run this with a different interpreter, try running `validator.be` to ensure your interpreter will work with my solution.

## Problem Summary ([?](https://adventofcode.com/2021/day/2))

**Part 1** gives us a list of commands, either `forward #`, `down #`, or `up #` for our submarine, where `#` is some digit.
After applying these as cartesian directions, we're asked to calculate the final horizontal and vertical displacement of the sub, and to multiply these together for submission.
The answer for my input is 1727835.

**Part 2** amends the way we interpret the instructions: instead of controlling depth, `down` and `up` control a concept known as "aim".
Now when we move `forward` by some distance `d`, we move the full horizontal distance as before, but also change depth by `aim * d`.
We're asked again to find the final horizontal and vertical displacement, and to submit their product.
The answer for my input is 1544000595.

## Retrospective

I've worked with [esolangs](https://en.wikipedia.org/wiki/Esoteric_programming_language) before (especially if you count [Zachtronics](https://store.steampowered.com/developer/zachtronics) games), but this is the first time I've written Befunge code.
I'm beyond thrilled that I got the opportunity to do so: having to do any complicated input parsing or use data structures more complex than an integer would have disqualified Befunge for me.
If even the input integers were multi-digit I probably would have passed on Befunge.
I really like it!
It feels like a more powerful(!?) version of the language in [Manufactoria](https://store.steampowered.com/app/1276070/Manufactoria_2022/) (which I've been playing a lot of recently), but with [NetHack](https://en.wikipedia.org/wiki/NetHack) graphics.

Part 1 went shockingly smoothly.
Track the x and y displacement on the stack, read inputs, adjust accordingly.
Befunge even has tooling to read digits vs characters.
What luxury!

Part 2 proved a bit trickier.
Befunge provides an operator `\` to swap the top two items on the stack, but offers no registers to dig any deeper than that.
It turns out maintaining `x` and `y` is simple, but maintaining `x`, `y`, and `aim` is a huge juggling act.
The only other storage you have access to in Befunge is _overwriting parts of the currently running program_ (not unlike a [certain other esolang](https://github.com/orez-/Advent-of-Code/tree/master/2019/day09)).
But this has its own caveats: the documentation for the `p` command states that it writes ASCII values to the program, but we're going to be working with enormous values.
Are we going to have to serialize and deserialize 32-bit integers into, like, four or five individual bytes?
It turns out the interpreter I found supports writing characters up to 2<sup>16</sup>-1.
This means we're able to keep the `depth` field in two characters on the program (since the depth field ends up going larger than 2<sup>16</sup>).
I imagine this is a nonstandard feature, but I'm pretty comfortable taking advantage of it.
Splitting `depth` over two fields like this is way more than twice as painful as keeping one field, but way less painful than storing it over five fields!

I ended up pre-editing the input file for easier consumption: essentially just removing all whitespace and newlines, and everything but the first letter and the digit from each command.
I gave some thought to supporting the full input, which would be easy enough from a code perspective.
Discarding a constant number of characters is straightforward to do, if a bit verbose.
I decided to not put the effort in though, because I'm not confident the interpreter I found supports inputs with newlines.
If I happen to find a local interpreter that can handle piping in a file I may revisit this, although the idea of having to edit an existing Befunge file is daunting enough that I likely will not.
