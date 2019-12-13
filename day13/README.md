# Day 13: Care Package

## Problem Summary ([?](https://adventofcode.com/2019/day/13))

Using the complete Intcode computer from [Day 9: Sensor Boost](../day09) ([?](https://adventofcode.com/2019/day/9)), run the code for a [Breakout](https://en.wikipedia.org/wiki/Breakout_(video_game)) style game.
The Intcode program will output updates to tiles by yielding the x coordinate, the y coordinate, and then the type of tile:

- 0 is an empty tile. No game object appears in this tile.
- 1 is a wall tile. Walls are indestructible barriers.
- 2 is a block tile. Blocks can be broken by the ball.
- 3 is a horizontal paddle tile. The paddle is indestructible.
- 4 is a ball tile. The ball moves diagonally and bounces off objects.

**Part 1** asks how many block tiles exist at the start of the game.
The answer for my input is 309

**Part 2** wants us to play the game to completion, moving the paddle via Intcode inputs.
It asks for our score at the end of the game.
The score is kept in coordinate -1, 0.
The answer for my input is 15410.


## Retrospective

Part 1 was dead simple, and I was quick enough and lucky enough to place very highly on the leaderboards.
This isn't exactly how I was hoping to make all my points this year, but I'll take it.

I felt like I was doing well on part 2 as well, but I ended up missing placing by more than a little.
I think I lost a lot of time preparing for debug, figuring out how to print the board.
Really I just needed to fetch ball position and paddle position, and work to align the two.

Looking around at how everyone else solved this one, I also saw some solutions that replaced the tape memory with more paddles or walls so they couldn't lose and didn't have to figure out how to move the paddle.
Very clever.
