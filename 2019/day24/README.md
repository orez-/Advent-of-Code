# Day 24: Planet of Discord

## Problem Summary ([?](https://adventofcode.com/2019/day/24))

This problem describes the lifecycle of bugs on a grid.
At each cell on the grid, if a bug doesn't have exactly one adjacent bug it dies, and if an empty space has one or two adjacent bugs it becomes infested.
Adjacency is defined as the four surrounding tiles, not diagonals.

**Part 1** asks us to simulate the board and find the first board that appears twice.
We're also provided a strategy to bitwise encode a board for the solution.
The answer for my input is 28772955.

**Part 2** changes the board to be recursive.
In the center square of our five by five grid is another five by five grid, with another five by five grid within that, and so on.
Similarly, our starting grid is the center tile on an outer five by five grid, and so on.
Adjacency rules still apply, but each tile may have more than four adjacent tiles now.
The puzzle input only defines the state of the starting layer.
All other layers start with no bugs.
We're asked to simulate this recursive board for 200 steps and count the number of bugs after this.
The answer for my input is 2023.


## Retrospective

Part 1's a pretty standard [cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton).
I lost a little bit of time trying to use a fancy `Board` class from my template that ended up being more trouble than it was worth.
I also had a bug (ha) where I was using the wrong variables to set new spots, resulting in my board growing (?!).
Managed to fix those up relatively quickly, and placed okay.
In terms of the leaderboard part 1 was truly a question of how fast you could implement it, not really a challenge of thinking up a solution.
I expected it to be pretty competitive.

For part 2 the trick of storing the board in a `dict` really shines.
Instead of `{(x, y): bug}` we store the board as `{(x, y, d): bug}`, where `d` is the depth in the recursion.
Since our adjacencies have become nontrivial we put together a function to find them, and we leverage that function to decide which tiles to run the update functionality against.
Now that we're working with a potentially infinite number of tiles we only want to look at tiles which may update, which is the tiles surrounding the current tiles.
Besides that the update code is largely the same.
I placed pretty well here.

I liked this problem!
The recursive board is a nice twist.
