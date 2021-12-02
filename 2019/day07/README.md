# Day 7: Amplification Circuit

## Problem Summary ([?](https://adventofcode.com/2019/day/7))

Building off of the Intcode computer from [Day 2: 1202 Program Alarm](../day02) ([?](https://adventofcode.com/2019/day/2)) and [Day 5: Sunny with a Chance of Asteroids](../day05) ([?](https://adventofcode.com/2019/day/5)), create five instances of the same program in sequence, and pipe the outputs from one into the inputs of the next.

**Part 1** has us assign the numbers zero through four to the instances, and to pass those first before starting the chain.
We're looking for the allocation that maximizes the final output.
The solution is that highest final output, and the answer for my input is 99376.

**Part 2** also has us maximizing output by allocating initial parameters, with the numbers five to nine.
However, in addition to yielding results from the last instance, we pipe that result back into the first instance to create a feedback loop.
The instances are not restarted during this loop.
The answer for my input is 8754464.


## Retrospective

Lots of fiddly details to mess up here.
I made an effort to read very carefully, and I think this helped out.

Ended up doing ok on part 1, but I completely missed on part 2.
Lost probably 40 minutes because I accidentally had all five tapes sharing and mutating the same memory list.
Gosh that's frustrating!
I miss Rust.
I'm not sure how I could've debugged that faster.
Trying to analyze the Intcode memory makes my eyes glaze over.
Duplicated the list in the tape definition now, so at least I shouldn't get bitten by this for the next Intcode question.
