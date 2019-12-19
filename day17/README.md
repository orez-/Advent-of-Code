# Day 17: Set and Forget

## Problem Summary ([?](https://adventofcode.com/2019/day/17))

This problem defines a map of dusty scaffolding, and a bot on that scaffolding who can turn and move forward, cleaning as it moves.
The scaffolding overlaps itself at some intersection points, but the entire scaffolding can be explored by walking straight through these intersections.
The scaffolding contains no other branches.

Our input is a shockingly featureful [Intcode program](../day09).

For **part 1** the Intcode program prints out an ASCII map of the scaffolding.
We're tasked with finding the coordinates of the intersection points, multiplying the x and y together for each, and summing each of these products.
The answer for my input is 6024.

In **part 2** the Intcode program acts as an interpreter for a language we need to input to it.
The main method defines a comma-separated list of submethod calls, either `A`, `B`, or `C`.
Next we define these three methods as either turning the robot `L`eft or `R`ight, or moving it an integral number of spaces.
To make things trickier, each of the main and sub- methods are limited to 20 characters, including commas.
The robot dies if it falls off the scaffolding, but each move outputs how much dust it has collected.
We are tasked with finding how much dust the robot has collected after it has touched each tile of the scaffolding.
The answer for my input is 897344.


## Retrospective

### Initial Solve

This one utterly kicked my ass.

I ended up placing very well on part 1 as a quick and dirty implementation problem, but I got completely overwhelmed by the possibilities in part 2.

I wrote a quick script to determine the commands required to walk the path, ignoring intersections.
However, I made the problem more complicated than it ended up being: instead of combining the steps into a single integer I left them each as a `1`-step.
My thought was we might potentially need to split the commands mid-walk, eg `A = 5,L,6` to handle `5,L,11,L,6` with `A,A`.
I also gave some consideration to over-turning, eg `A = 17,L`, `B = R,11` covering `17,L,17,L,28,R,11` with `A,A,A,B,B`.
In the end neither of these considerations featured in the solution!
Turns out the 20 character limit comes at you fast, especially with the commas.
No room to do anything tricky; we ignore the intersections, and all of our commands are of the form `(turn,move)+`.

I put together a function to try to take substrings of my `1`-step string and find repeats of em, but I had trouble tuning what exactly I was optimizing for.
As it became more and more clear I wasn't going to find a result this way I tried to identify substrings by hand, but still on the `1`-step string.
This was a huge pain in the ass!
Only after I compiled them to the `(turn,move)+` format was I able to identify the cut points by hand, well after everyone else had finished.

I may have had more luck with the solve algorithm recognizing that we could say the start of the path string is unconditionally the start of `A`.
I may revisit this problem keeping that in mind.

### Wrapping up

Despite all this, I'm a big fan of this problem.
It's definitely a unique one.
I'd be interested in actually putting together a solution for the more general cases I mentioned above.

It's important to remember that the goal of Advent of Code isn't always "get the computer to print out something you can copy and paste to the output field", it's simply "get the right answer as fast as possible".
Similar to how you wouldn't OCR the problems where you [print pixels of text](../day08), the goal is to build something to get information that you the human can interpret to find the answer.
I took too long to recognize this today, and it bit me.

Final thoughts:

- I'm impressed that this puzzle uses Intcode to print maps and error messages.
  It's proven to be a shockingly expressive little language.
- I'm glad I added queuing multiple inputs between this and the last Intcode problem.
- I want to call out how much I love [this solution](https://github.com/mastermatt/advent_of_code/blob/264734984d2f396b0cff115038d919bff552ac67/2019/day17/index.js#L106-L112).
