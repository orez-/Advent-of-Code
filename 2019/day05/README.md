# Day 5: Sunny with a Chance of Asteroids

## Problem Summary ([?](https://adventofcode.com/2019/day/5))

Starting with the Intcode computer from [Day 2: 1202 Program Alarm](../day02) ([?](https://adventofcode.com/2019/day/2)), add a few more instructions and the concept of immediate mode parameters.
By default instructions use position mode parameters, which means they refer to memory addresses.
Immediate mode parameters refer to values directly.
A parameter's mode is defined by the digits of the opcode: 100s digit for the first parameter, 1000s digit for the second parameter, and (theoretically) so on.

**Part 1** introduces a command to write a single input value to memory, and a command to print a single value from memory.
The answer for my input is 6745903.

**Part 2** introduces commands for jump if true, jump if false, less than, and equals.
The answer for my input is 9168267.


## Retrospective

I spent some time this morning putting together a nice Intcode runner, trying to anticipate what additional features might be needed and trying to keep the code as extensible as possible.
Having the parameter grabbing code in particular was a big help; I didn't have to worry about bad copy paste when fetching parameters and advancing the instruction pointer.
I certainly didn't predict the immediate mode thing, but I'm still very suspicious of the fact that the spec hasn't explicitly defined that the instruction pointer going out of bounds is illegal.

My part 1 went pretty smoothly.
My first diagnostic test failed but I decided to try submitting the solution I got anyway, and it worked.
It turns out the test failed because I forgot to support immediate mode for the output.

Spent a lot of time debugging part 2.
I kept overflowing the tape.
Went back and solved the issue I had with part 1 in hopes that that was the issue, which burned a lot of time.
In the end it turned out I had just swapped the immediate mode check on the jump commands, which meant that instead of jumping to register 238 I was jumping to the _value_ of register 238, which was out of bounds.

If I had defined the position mode check and conversion in the `grab_parameters` function I may have avoided this issue.
However, it was a very intentional decision on my part to not do this for the initial solve.
I didn't want to have to write out how to check an arbitrary digit of a number of potentially fewer digits under the time constraint.
I believe having to debug that would've been a poor use of time.
In addition, parameters used as output addresses needed to NOT get converted, which would mean more edge cases in `grab_parameters`.
Better to just hardcode the check as needed.
Despite losing a lot of time here, I think this was the right decision.
