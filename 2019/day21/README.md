# Day 21: Springdroid Adventure

## Problem Summary ([?](https://adventofcode.com/2019/day/21))

The problem input is an [Intcode](../day09) program that interprets a simplified assembly language "springscript".
Springscript programs operate on booleans, and have two writable registers: `T` the temporary value register, and `J` the jump register.
Both start as false, and when the jump register is true the springbot will jump.
We also have the ability to view if there's ground ahead of us with the read-only registers `A`, `B`, `C`, and `D`.
`A` checks the spot one ahead, `B` two ahead, and so on.
If there's a hole the register is false, if there's ground it is true.

Springscript contains the following commands:

- `AND X Y` sets `Y` to true if both `X` and `Y` are true; otherwise, it sets `Y` to false.
- `OR X Y` sets `Y` to true if at least one of `X` or `Y` is true; otherwise, it sets `Y` to false.
- `NOT X Y` sets `Y` to true if X is false; otherwise, it sets `Y` to false.

In addition the final command in the program should be `WALK`.

Our goal is to craft a springscript program to allow the springdroid to get to the other side, regardless of terrain.
On a successful run the droid will return some integer: our puzzle's solution.

The answer for my input in **part 1** is 19353619.

**Part 2** replaces the `WALK` command with a `RUN` command, which adds the registers `E`, `F`, `G`, `H`, and `I`, for the fifth through ninth spaces away.
We're tasked with anticipating and reacting to more treacherous terrain.
The answer for my input is 1142785329.


## Retrospective

I basically just started adding conditions to accommodate failing tests.
I'm not even entirely convinced my solution handles every possible case it could, but it handles all the cases my program input threw at me.
Since the droid jumps four squares each time, we try to jump as early as possible in a way that doesn't leave us in a bad position later.

I guess I could've pulled the `AND D` condition to the outside, since we never want to jump in a hole. Oh well.

This register juggling reminds me of the assembly programming game [Exapunks](https://store.steampowered.com/app/716490/EXAPUNKS/).
Check out Exapunks, it's a fun one.
