# Day 2: 1202 Program Alarm

## Problem Summary ([?](https://adventofcode.com/2019/day/2))

This problem defines the Intcode language.
Intcode programs are a list of comma-separated integers, whose commands overwrite _the program itself_.
There is no other storage!
Bytecode metaprogramming.

Each cycle we read the value at the instruction pointer to decide what command to run and how many arguments to consume.
After each command we move the instruction pointer past the command's arguments.

To start we're only asked to define commands for addition (opcode 1), multiplication (opcode 2), and halt (opcode 99).
Addition and multiplication's arguments refer to memory addresses, so `1 5 8 9` says `memory[9] = memory[5] + memory[8]`.

**Part 1** asks to override `memory[1]` and `memory[2]` with specific values, and return the value in `memory[0]` when the program terminates.
The answer for my input is 4690667.

**Part 2** asks to find the values to override `memory[1]` and `memory[2]` with, such that `memory[0]` is some given value.
These values are guaranteed to be between 0 and 99 inclusive.
The answer to submit is `memory[1]` concatenated to `memory[2]`.
The values for my input were 62 and 55, so the answer is 6255.


## Retrospective

The fact that Intcode uses the program itself as memory definitely took a few rereads to understand.

I tried keeping the list of commands as strings for some reason, and when I realized it was going to be easier to int-ify everything at the start I forgot to update my opcode comparison to integers.
Burned some time there.

I copy pasted the addition code for multiplication, and forgot to actually update the operator.
Burned some time there.

I lost a bunch of time to the fact that the test cases didn't want the part 1 value override, and forgetting to add the override back in.

I skimmed over the part that mentioned part 2 was only looking for values between 0 and 99.
I got really intimidated by the prospect of dovetailing those values to infinity before I noticed the constraint.
I really need to slow down and read these problems more carefully.

I added some quick checks for timeouts and out-of-bounds, which was probably a bad use of time.
There's no looping yet so timeouts aren't an issue, and none of the inputs send the instruction pointer out of bounds.
In fact, the fact that an out-of-bounds instruction pointer doesn't have defined behavior makes me suspect a future problem will do something interesting with this case.

Unsurprisingly, I didn't place! Next time.

I appreciate that the problem calls out that Intcode is going to be reused in future problems this year.
In previous years I've had to scramble to clean up old solutions to reuse later.
