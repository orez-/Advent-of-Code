# Day 18: Many-Worlds Interpretation

## Problem Summary ([?](https://adventofcode.com/2019/day/18))

The problem input describes an acyclic maze filled with 26 doors, with a corresponding 26 keys.
We are tasked with moving a robot around the maze to collect all the keys in as few steps as possible.
We can only pass by a door when we have collected the key of the corresponding symbol.

**Part 1** asks how many steps are in the fewest-steps walk.
The answer for my input is 4248.

**Part 2** alters the layout of the center of the maze to create four separate mazes, run by four separate robots.
The robots share collected keys, and the goal is still to find the minimum number of steps to collect all the keys.
The answer for my input is 1878.


## Retrospective

### Original solution

This one was tougher than it may initially seem!
I spent a _lot_ of time just on part 1, and the leaderboard suggests I wasn't the only one.
Clearly at any moment we only ever want to move toward some key, so this becomes reducible to deciding the order in which to go to the keys.
But ignoring doors there are `26!` such possibilities; that's a 4 and then (coincidentally?) 26 zeroes.
That's a lot!

My original solution defined a method to find the state of the board if we moved to any of the different accessible keys.
I first tried using this method in a recursive search of all possibilities, which was just a comically optimistic move on my part.
I ended up replacing this recursive search with an [A* search](https://en.wikipedia.org/wiki/A*_search_algorithm) to traverse board states, in an attempt to prune clearly bad decisions.
The heuristic I chose for the search was essentially worthless though, reducing my search to [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm).
Still, this managed to be enough of a boost to get me the answer.
My part 1 takes 5m31s to run, but it finds the right answer!

Modifying the code I had to support part 2 ended up being very straightforward.
I had to update the possibility space search to start from the four different robots instead of just the one.
My part 2 takes 6m47s.
Somehow I got this together in time to place 79th, after 105 minutes.
Like I said, this was a tricky one!

In terms of implementation challenges, I lost some time throwing an `lru_cache` on a generator function.
Rookie mistake: it caches the generator all right, which is consumed after the first iteration.
This caused the `next_goals` function to erroneously report no further keys to find sometimes, which in my haste I took to mean we had completed the task.
Overall though most of my time was spent trying to make my solution more efficient, which was what the problem was trying to exercise.
So, mission accomplished!

### There must be a better way!

After finishing the race, I went back and tried a [slightly different solution](cleanup.py).
Since the maze _is_ acyclic (not a property mentioned in the problem!) I tried precomputing the paths between all keys<sup>[1](#footnote1)</sup>.
I created a dictionary mapping starting key to `Path`, where a `Path` is:

- a destination key
- any doors we need to open to get between them
- any keys we'd pick up on the way (including the destination key)
- and the number of steps to get there.

I also calculated `Path`s _from_ the robot starting positions but not _to_ them, to perform the first step of the journey.
Once this was in place I was able to discard the rest of the board data and only operate on this path data.
Notably we never operate on coordinates or walls again!
Our robot positions from here on out are tracked by which key they're standing at.

Tracking a `State` object of collected keys and robot positions, we're able to use our Dijkstra's algorithm again (simplified to an actual Dijkstra's algorithm instead of a neutered A* ) to move between `State` adjacencies.
We generate states by moving each of the robots to each of the different keys they can reach (that there exists a path to, and we have all the keys for the doors encountered on the way), picking up any keys encountered along the way and noting the distance traveled.
We also make sure we never revisit a key we've already picked up, as there's no reason to revisit that spot.

This ended up doing the trick.
My parts 1 and 2 combined take 4 seconds total with this strategy.
I like this solution a lot, it feels very clean.
Compiles the information it needs, discards the information it doesn't, and doesn't really have any thorny special cases.

### Wrapping up
I'm a big fan of this problem, despite (or maybe because of) the fact that it kicked my ass.
I've mentioned on previous days that I'm a big fan of problems with simple definitions that belie their complexity and difficulty to solve.
I had a lot of fun putting together the cleaned up faster solution as well, even if it absolutely wrecked my sleep schedule.

It'd be remiss of me to not mention that python's [`heapq`](https://docs.python.org/3.7/library/heapq.html) module remains one of the most unpythonic, frustrating stdlib modules to work with.
It doesn't have a way to separate the priority from the value, so you either end up having to throw both into a tuple (and hoping your value is orderable, as a tiebreaker!), or creating a custom class each time to hold both values and only compare on the key.
And it avoids creating its own datastructure for the heap, using a plain `list` (that it keeps in heap-order).
But not for duck-typing reasons: trying to use a [`blist`](https://pypi.org/project/blist/) to improve performance results in `TypeError: heap argument must be a list`.
Why then??

It's also difficult to change the priority of an element in the heap, although this might be more of an issue with the hand-wavey pseudocode definitions of the Dijkstra's and A* algorithms than the `heapq` module.

Worth calling out this is the first time I've used [`dataclasses`](https://docs.python.org/3.7/library/dataclasses.html) on an Advent of Code!
They're great, and they did great for me here.
I also ended up using my old go-to the [`frozendict`](https://github.com/slezica/python-frozendict) module for my original solution, which I'm still a little mad python [hasn't added](https://www.python.org/dev/peps/pep-0416/) into the stdlib ([yet???](https://www.python.org/dev/peps/pep-0603/)).

---

<a id="footnote1">1</a>: If the maze hadn't been acyclic this would have been a lot trickier.
Consider a section:

```
#########
#d......#
#.#####.#
#A#####B#
#.#####.#
#.......#
####.####
####c####
####.####
```

Our Dijkstra's algorithm would want to know about both the left and the right path from `c` to `d`, noting the unique requirements of each.
But our BFS precompute step currently short-circuits on cycles.
Just discovering these paths would require extra consideration.
