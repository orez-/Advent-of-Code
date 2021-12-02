# Day 14: Space Stoichiometry

## Problem Summary ([?](https://adventofcode.com/2019/day/14))

The input file describes recipes for converting some amount of reagent materials to an amount of some other product material.
The amount created is indivisible.
That is, if a recipe creates 10 FOO, it is not possible to use the recipe to create less than 10 FOO, or any amount except a multiple of 10.
The puzzle mentions that each material only shows up once in the product list, ie there's exactly one way to create each material, except for ORE which is a base material and has no recipe.

**Part 1** asks us to find the amount of ORE required to create one FUEL.
The answer for my input is 397771.

**Part 2** gives us a budget of one trillion (1000000000000) ORE, and asks how much FUEL we can create.
The answer for my input is 3126714.


## Retrospective

I had a lot of fun with this puzzle.
I was a little worried I was wasting a lot of time on part 1, but I ended up placing pretty well, top 50.
My first solution for part 1 didn't take into account excess material, and in order to support this I ended up having to come up with meaningful names for my variables instead of just `t` or `c` or `groups`.
But once everything was named, reasoning about it became much easier, and the solution fell into place.

For part 2 I briefly considered the effort it would take to swap the recipe order kind of, to build up from ORE instead of down from FUEL.
I can't even imagine now exactly how I'd do this.
Instead I just reran my part 1 code for increasing FUEL amounts, until I surpassed the ORE budget.
This on its own ended up being far too slow, so instead of iterating to a trillion I iterated to
a billion (in ~5 seconds) and multiplied the resulting FUEL by 1000, making that my new starting point.
This got me the answer pretty quickly, placed even better for part 2.

I actually ended up overcorrecting: took care to return the FUEL _before_ surpassing the ORE budget, but then also manually subtracted one before submitting.
Lost a minute there.
A little frustrating, but can't complain.
Will have to be more careful going forward.
