# Day 8: Seven Segment Search

**Language: [Haskell](https://www.haskell.org/)**

## Usage

Installation instructions for Haskell can be found at https://www.haskell.org/downloads/

```bash
ghc part1.hs && ./part1 < file.txt
ghc part2.hs && ./part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/8))

In today's puzzle our four-digit seven-segment displays have their outputs scrambled.
The good news is they're scrambled consistently (per line in the file).
Eg, if segment `c` is instead mapping to `d`, all `c`s will map to `d`s.
Each line in our input file contains the outputs of the scrambled digits 0 through 9 in some order, followed by four more digits representing the display.

This one's complicated, probably just read through the official problem statement.

**Part 1** notes that 1, 4, 7, and 8 can be identified unambiguously, since we know how many of their segments are lit up and no other digit share their number of segments.
We're asked to count how many digits on our display are 1, 4, 7, or 8.
The answer for my input is 362.

In **part 2** we're asked to perform the full decoding, and find the sum of all the four-digit displays.
The answer for my input is 1020159.

## Retrospective

Part 1 today was a pretty straightforward "do you understand the input" test, which I appreciated because it definitely took me a few rereads to understand exactly what the input was expressing.
I really like that part 2 was a puzzle solving exercise more than a programming exercise.
I like that there's a bunch of different but totally valid approaches here too.

Today's problem felt like a step up in complexity.
I was kind of hoping to use a goof-around challenge language today, but the thought of having to parse that input dissuaded me quick (to say nothing of actually solving the problem).

Which isn't to say I'm not excited I got a chance to write some Haskell!
I have played around with Haskell a very little bit in the past, but that was close to a decade ago.
I like it!

Some Haskell thoughts:
- Going into this I didn't realize Haskell has syntactically significant whitespace!
  I lost some time to this trying to debug an unhelpful `parse error on input 'if'` error message (or whatever the next token happened to be).
  I didn't end up finding the documentation for the whitespace rules either.
  I'd just indent a bunch until my `do` blocks stopped hollering.
  I'm cool with significant whitespace, but speaking as a fool I think it's safe to say that Haskell's methods of guiding users to proper usage of whitespace are not foolproof.
- Other than this one speedbump though, Haskell's error messages were pretty helpful!
  Good tracebacks, explanations for how it had tried to read the code, what went wrong, what I probably meant instead.
  For some of the errors the wording was a little unclear to me, but most of the messages referred to unambiguous concepts that I was able to look up.
  Which was good, because:
- Function associativity kicked my ass.
  The rules for parens in Haskell are way different from what I'm used to, and as a result I ran into a lot of compile time errors about passing the wrong arguments to the wrong functions.
  I [learned about `$` and `.`](https://typeclasses.com/featured/dollar) at some point which are very cool and helped combat this a little, but I think armed me with just enough knowledge to be dangerous.
- I get the sense I really butchered this code.
  Like a pro Haskellite would look at it and shake their head and cry.
  "No," they would say.
  "Not like this."
- Even so, I had a lot of fun!
  Love to `filter` and `map` and `foldl`.
  I'd totally be down to dig deeper into Haskell.
