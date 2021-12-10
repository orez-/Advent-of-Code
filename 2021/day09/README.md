# Day 9: Smoke Basin

**Language: [Idris 2](https://www.idris-lang.org/)**

## Usage

Installation instructions for Idris can be found at https://www.idris-lang.org/pages/download.html .
I found it easiest to just `brew install idris2`.

```bash
idris2 part1.idr -o part1
idris2 -p contrib part1.idr -o part1
./build/exec/part1 < file.txt
./build/exec/part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/9))

Today's input describes a height map: each digit represents the height at that location.

**Part 1** asks us to find all the local minima, and sum their heights+1.
The answer for my input is 480.

**Part 2** defines 9s as ridges delimiting basins.
We're asked to find the largest three basins by area (ignoring depth), and take the product of their areas.
The answer for my input is 1045660.

## Retrospective

Ha ha wow this one kicked my ass.
I took a VERY long time trying to piece it together.
I've done problems like this one hundreds of times before, but this is the first time I've tried to do one without mutable state!

For part 1 I almost certainly overcomplicated it.
I didn't find the `index` function until part 2, so I needed some other way to find the elements surrounding each cell.
I put together a `windows3` function to get every three consecutive elements from a list (with a little overhang to catch the edges).
Then I can just `map` that over the rows, and `windows3` those mapped rows.
Perfect, right?

Wrong!
So far we have `List (List a) -> List (List (a, a, a), List(a, a, a), List(a, a, a))`[^busy], which is..busier!
But not what we need yet.
Now we `map` `zip3` over the outer list, concatenate all the resultant elements together, and perform one last conversion to get a `List (a, List a)`: a list of each element and its adjacent elements.
Filter out the ones we want and sum em up, and there's our answer!
It's as easy as that, or at least no harder than that 💀.

For part 2 it became pretty clear we wouldn't be solving this without the `index` function, so I managed to track that down.
The algorithm I ended up with is pretty standard: we've got a recursive depth first search, which we run over every cell on the board.
The only unusual part is the "statefulness": we want to track a set of the spots we've already seen[^alternate_solution], not only through one run of the DFS but all time.
We only need to count each cell once after all.
Once we've counted it for one basin, we don't need to check it again.
Since we can't mutate state though, we instead have our DFS function return the seen set updated with the spot we just checked.
Then we can pass that updated state into the next DFS call.
The outer `foldl` that coordinates checking every cell is pretty wild... I'm not sure this is exactly how you're supposed to do it, but I'm happy I managed to get it working.

Idris thoughts:
- Oh my god Idris uses terminal formatting in its errors.
  This is so nice.
  I ran into a lot of unhelpful "parse error: you have failed somewhere" errors which wasn't great. But type inference errors with the full expected type, full actual type, and just the part that failed to mesh, all layed out clearly and colorfully?
  Beautiful.
- Idris is eager, with types to mark [Lazy variables](https://idris2.readthedocs.io/en/latest/tutorial/typesfuns.html#laziness), and tooling to unpack Lazy fields as needed.
  I think I don't fully understand the implications of the decisions here.
  It seems to me having everything as lazy as possible is a valuable property, but if there's some tradeoff that makes that undesirable I quite like the idea of a Lazy type with seamless execution as needed.
- Idris 2 is very similar to Idris 1, but it's just different enough that it was pretty frustrating to find outdated info in the Idris 1 docs.
  - The change that really bit me was they changed the `index'` function from [returning a `Maybe`](https://www.idris-lang.org/docs/current/prelude_doc/docs/Prelude.List.html#Prelude.List.index') to [enforcing length](https://www.idris-lang.org/docs/idris2/current/base_docs/docs/Data.List.html#Data.List.index') with `Fin` (instead of having you write your own proof as with `index`).
    Augh.
- Another consequence of the version split is the documentation feels a little scattered, tough to track down.
  Once I did find the official documentation for whatever feature I was looking for though, it was phenomenal.
  Clear and to the point, plenty of examples.
- I ended up fudging my solution exactly once in each part 1 and 2 by hardcoding the width of the input (look for the `100`s in the code).
  Each of them is interesting in a different way:
  - In part 1, as defined, there is _no_ way to infer the width there.
    We're constructing an empty row from a single `Nothing` element, there's nothing to indicate how wide that should be.

    I think the way to solve this is with a [dependent type](https://idris2.readthedocs.io/en/latest/tutorial/typesfuns.html#dependent-types), ie a [`Vect`](https://idris2.readthedocs.io/en/latest/tutorial/typesfuns.html#list-and-vect).
    Then we can pull the width off the type.
    By the time I had realized this might be valuable though, I was several hours into a solution that leveraged `List`s instead.
    Went with the hardcoding.
  - In part 2 we want to enumerate all 10,000 spots in the map, and we do this with a [list comprehension](https://idris2.readthedocs.io/en/latest/tutorial/typesfuns.html#list-comprehensions).
    We enumerate the ys, `0` to `(length board)`, but enumerating the xs is a little trickier.
    We could take the length of the first row of the board, but as far as Idris knows the board might not have _any_ rows.
    We could take the length of the row we're currently looking at in the ys (probably more accurate anyway), but Idris isn't convinced that row exists either.
    It wants a [proof](https://www.idris-lang.org/docs/idris2/current/base_docs/docs/Data.List.html#Data.List.InBounds) that y exists in the board.
    I wasn't prepared to sit down and learn a new paradigm after such a long solve, so close to the finish line, so I went with the hardcoding.

  It's absolutely a shame that I wasn't up for learning about these things.
  These are the two big things that make Idris stand out (the syntax and flow seem otherwise nearly identical to Haskell).
  Now that I have the baseline familiarity with the language I want to give this another shot sometime.

Overall I had a TON of fun with this.
I'm sure the code I managed to scrape together here was amateurish (if in no other way than literally), but there's no question in my mind that I want to learn more Idris in the near future.

[^busy]: give or take a few `Maybe`s, which didn't serve to make this LESS complex.
[^alternate_solution]: Come to think of it, it may have simplified things a little to keep a set of spots to visit, rather than spots to avoid.
Then we could handle the 9s check up front, and skip the out of bounds check altogether.
We wouldn't even have to pass the board around anymore!
