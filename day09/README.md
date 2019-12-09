# Day 9: Sensor Boost

## Problem Summary ([?](https://adventofcode.com/2019/day/9))

Building off of the Intcode computer from [Day 2: 1202 Program Alarm](../day02) ([?](https://adventofcode.com/2019/day/2)) and [Day 5: Sunny with a Chance of Asteroids](../day05) ([?](https://adventofcode.com/2019/day/5)), add the concept of relative mode parameters.
Relative mode parameters are specified in the opcode like immediate mode parameters, specified by the digit 2.
A relative mode parameter acts as a position mode parameter, but offset by a global relative base.
The relative base value can be adjusted by opcode 9, which adds its only argument to the relative base.

We also update the memory tape to be unbounded.
Any addresses not specified in the program definition default to 0.

The problem mentions that this is the full Intcode language definition.

**Part 1** runs with an input of 1.
The answer for my input is 3063082071.

**Part 2** runs with an input of 2.
The answer for my input is 81348.


## Retrospective

I gotta say, I really wish they had spaced out these Intcode problems further.
I'm very looking forward to solving problems that aren't debugging this same Intcode compiler every other day.
Since they mention this is now the complete Incode computer I'm hopeful there's at most one more day of Intcode, where they have you analyze an Intcode program that's too slow to just run, similar to 2018's [Day 21: Chronal Conversion](https://github.com/orez-/Advent-of-Code-2018/tree/master/day21) ([?](https://adventofcode.com/2018/day/21)).
Or maybe another similar to [Day 7: Amplification Circuit](../day07) ([?](https://adventofcode.com/2019/day/7)) where you use a bunch of them in sequence in some interesting way.

I did real bad!
Previously I had had to special-case the final "write" parameter for some commands to skip the position mode transformation, since we need to pass back an index to update
(I guess technically I could've kept each instruction in some wrapper object and unconditionally return that, but... no).
But we still need to apply the relative mode transformation, so I had to scramble to special-case that too, and I was very slow in debugging the issues I had making the change.
Ran into the issue where I forgot to swap my input back from my debug input, that old classic.

Making the tape infinite was easier than I expected.
I only had one slice access, so I just had to convert that to discrete lookups and then convert the memory to a `defaultdict` instead of a `list`.
I guess that's the benefit of having a nice API and not having a bunch of callers digging through the internals.

Having part 1 try to act as a diagnostic check that actually outputs the opcode in error is slick as hell.
Huge props to the Advent of Code team for that detail.
