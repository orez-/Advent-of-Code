# Day 25: Cryostasis

## Problem Summary ([?](https://adventofcode.com/2019/day/25))

This problem provides an [Intcode](../day09) script for a simple interactive fiction game.
We're able to move in the cardinal directions, take items from the room, drop items in the room, and check our inventory.
There exists in the maze a door that can only be opened with the correct combination of held items.
The only hint we get is the feedback if our current load is too light or too heavy.
In addition, there exist some items which make you lose the game if taken.
We are tasked with "exploring the maze for the password".

Day 25 only really has a **part 1**, and the answer for my input is 35717128.


## Retrospective

Interesting problem.
In past years Day 25 has been a relatively simple and quick puzzle, and I feel this wasn't exactly that.
Given the pitfalls of the items which kill you, I assume we were meant to build a quick shell over the game to play it manually.
But trying all 256 different combinations of items at the door sure sucks!
I ended up getting to the door manually before deciding to rig something to check the door, and eventually deciding to automate solving the whole thing.
This took a lot of time, and I didn't place.
Fortunately most of the other regulars on the leaderboard did not place either, so my overall ranking didn't shift very much.

Trying all the items against the door is simply enumerating the [powerset](https://en.wikipedia.org/wiki/Power_set).
However each `take item` and `drop item` takes a non-negligible amount of time.
I never ended up explicitly tracking what items we're carrying: my first solution had us try to drop each item (discarding the error message if we weren't carrying it), then take only the items we needed.
For my improved after the fact solution, I only dropped the items I wasn't going to immediately pick up again.
I remembered though that there was some algorithm to enumerate the power set making only one change at a time, and after some searching I ended up finding an example: [Gray code](https://en.wikipedia.org/wiki/Gray_code).
I updated my better solution to remove or add one item at a time and check the door after each change, taking the worst case down from `2ⁿ * n` to just `2ⁿ`.

Besides the items-that-kill-you, a few other quirks made this tough to solve:
- I'm pretty sure the world loops over itself, eg north->west and west->north may take you to two different rooms.
  My original approach of mapping out the world in coordinates tripped over this.
  Ended up having to track the rooms by name instead.
- The problem statement says that it accepts commands after the word "Command?", and I tried to shortcut this by checking for a "?".
  Turns out other text had a "?" as well, which caused a few issues.
  Alternatively it would've been nice to have had a system in place for my Intcode interpreter to block on missing input, instead of having to check for "Command?" (and having to make sure we advance the text if we input multiple commands).

I'm not the biggest fan of quirky puzzles like this one, but it's kind of a neat change of pace for the final day.
I'm still super impressed that Intcode can represent a program of this complexity, with this much raw text(!) in such a relatively terse little script.

Fun closing note: this was my first and only depth-first search of the year!
Lots of breadth-first, only one depth-first.
