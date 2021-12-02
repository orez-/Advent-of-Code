# Day 19: Tractor Beam

## Problem Summary ([?](https://adventofcode.com/2019/day/19))

The given [Intcode](../day09) program can be queried to check if a coordinate is affected by the tractor beam or not.
The tractor beam is an infinite "2d cone", eg the area between two diverging lines.

**Part 1** asks how many squares in the 50 by 50 square area in front of the emitter are affected by the tractor beam.
The answer for my input is 220.

**Part 2** asks us to find the closest point to the emitter where we can entirely fit an axis-aligned 100 by 100 square in the tractor beam.
We specifically want the coordinate of the top left corner of the square.
The coordinate for my input is `1001, 825`, which is translated to the answer 10010825.


## Retrospective

Short short puzzle today, presumably to cool off after [yesterday's](../day18).

Part 1 is trivial, and I placed pretty well.

For part 2 I decided to walk the bottom edge of the tractor beam, and to check the coordinate 100 by -100 away until it was also in the tractor beam.
To walk the edge I start at a point known to be in the beam, then either move down if we're in the beam or right if we're not in the beam.
And.. that's it!
I think there were a handful of edge case things to get wrong here, but everything came together without much hassle for me.
I ended up placing [sixth overall](https://adventofcode.com/2019/leaderboard/day/19)!
Can't complain about that at all.

I feel like this problem expected to trick me in some way or something, like there should've been more to it.
I guess the naive approach would be to map out the entire area to find the square, but calling the Intcode program seemed slow and crappy, and honestly identifying squares in an image seems like a huge pain in the ass.
It didn't occur to me to try this, which is for the best.
I guess you could also try doing something tricky calculating the slope, but again why bother?
