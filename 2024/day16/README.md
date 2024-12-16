# Day 16: Reindeer Maze

## Usage

```bash
cargo run --bin day16 part1 < input.txt
cargo run --bin day16 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/16))

Today's problem has us navigate a maze, minimizing cost.
Moving costs 1, turning costs 1000.

**Part 1** asks for the cost of the best path.
The answer for my input is 111480.

**Part 2** wants to know how many tiles are part of at least one of the best paths through the maze.
The answer for my input is 529.

## Retrospective

Whew! _Now_ we're getting into it!

Part 1 is a standard best-first search.
I ended up cutting a corner by only allowing a rotation if you're able to move off of it, which was cute, if not strictly required.

Part 2 legit stumped me for a while!
I did misunderstand the requirement briefly, spent some time thinking about how to find the number of tiles which are tied for touched by the most paths[^1].
But even when I was solving for the right thing, I got hung up on my turn-and-move pattern for a good while.
I ended up undoing the turn-and-move optimization, having instead two turns and a move as options.
After that, I did a search from `start` to all[^all] states (position * facing), and separately a search from `end` to all[^all] states, then counted all states which had entries in both maps which summed to our `best` value.
I'm certain this is some Named Algorithm.
But I don't know which one it is, so I'm happy to have re-derived it.
The only tricky thing here is going _from_ end _to_ all states means our heading is backwards at each step when compared to the from-start states.
This is easy enough to handle though: we ensure the initial states of the from-end search include all starting directions, and flip the `facing` when we compare against from-start states.

I ended up not needing a [`BinaryHeap::into_iter_sorted`](https://doc.rust-lang.org/std/collections/struct.BinaryHeap.html#method.into_iter_sorted), but I did need a [`HashMap::try_insert`](https://doc.rust-lang.org/std/collections/struct.HashMap.html#method.try_insert), and both are nightly-only.
Rust sure does have a lot of fundamentally useful yet nightly-only methods!

[^1]: which, in retrospect, isn't _such_ an interesting problem. Since the start and end exist in all paths, this is essentially "how long is the required common path leading into and out of the maze".
[^all]: technically we prune states which take longer to reach than the goal, as an optimization.
