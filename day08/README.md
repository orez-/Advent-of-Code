# Day 8: Handheld Halting

## Problem Summary ([?](https://adventofcode.com/2020/day/8))

This puzzle introduces a simple bytecode language where each line is a command and a signed integer.
- `acc` adds the integer to a global accumulator register
- `jmp` jumps relative to the instruction by the amount in the integer
- `nop` does nothing

The given program is stuck in an infinite loop.

**Part 1** asks for the value in the accumulator just before the first repeated command.
The answer for my input is 1744.

**Part 2** asks us to either flip one `jmp` into a `nop`, or one `nop` into a `jmp`.
We're looking for the flip which will allow the program to terminate by attempting to run the command just after the last line of the program.
We're tasked with finding the accumulator value of that program.
The answer for my input is 1174.


## Retrospective

Back to [bytecode interpreters](https://github.com/orez-/Advent-of-Code-2019/tree/master/day09), the [bread](https://github.com/orez-/Advent-of-Code-2017/tree/master/day18) and [butter](https://github.com/orez-/Advent-of-Code-2017/tree/master/day23) of Advent of Code.
Having done this kind of problem in previous Advent of Codes definitely helped me here.
I always have to fight the urge to iterate the commands with a `for` loop (which would make handling `jmp`s difficult).

Part 1 was pretty straightforward.
Implement the interpreter, and keep a set of seen line numbers.
Check for repeats with that, and we're good.

For part 2 I ended up brute forcing all the possible swaps, and calling out to my existing part 1 code to run the interpreter.
I modified the part 1 code a little to raise an exception with the accumulator value when it steps out of bounds, which I let bubble up and halt the program.
This is [another](../day05) situation where having a human (me) parse the last leg of the output is faster than trying to figure out how to display it nicely.

It does mean my code for today is pretty hideous though ᖍ(ツ)ᖌ

I spent some time making sure the terminating jump jumps to the correct spot to protect against jumping _past_ the end of the program, but it looks like this case never comes up anyway.
Oh well!

I placed in the mid 20s for both parts!
Very pleased with this.
