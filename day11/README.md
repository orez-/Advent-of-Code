# Day 11: Space Police

## Problem Summary ([?](https://adventofcode.com/2019/day/11))

Using the complete Intcode computer from [Day 9: Sensor Boost](../day09) ([?](https://adventofcode.com/2019/day/9)) as the brain to a robot, model that robot's behavior in the world.
Starting on an infinite canvas of black squares:
- read the color of the current square as input to the program (0 for black, 1 for white)
- write the color the program outputs
- read another output and turn left (0) or right (1)
- move forward
- repeat until the program halts

**Part 1** has us count the number of squares that get painted at least once.
The answer for my input was 2056.

**Part 2** has us change the starting square to white initially, and print out the resulting painted text.
The answer for my input was GLBEPJZP.


## Retrospective

Cooool, more Intcode 😓.
I guess thinking on it further it's neat that we've been charged with creating our own black-box calculation engine.
Sure is hostile to the people who do this in a different language each day though.

This one came together pretty quickly for me.
No trouble modeling the board and the bot position.
Had to update my Intcode computer so the outputs actually went somewhere, but this ended up being a pretty quick fix.

For part 1 I got a "TypeError: not all arguments converted during string formatting" on line `code = self.head() % 100`, which really threw me for a loop.
Had to google it, but I figured it out pretty quickly: in my hasty copy paste I forgot to int-ify the Intcode file, so `self.head()` was a string and the `%` operator was doing interpolation.
Easy fix.

For part 2 I got a big horrible mess instead of text, because while I had updated the board with the initial white square I never updated the Intcode progam's input value.
Lost more time than I wanted debugging that.

I placed low on part 1, and barely placed at all part 2.
It's been a rough couple days though.
I'll take it.
