# Day 13: Transparent Origami

**Language: [Miranda](http://miranda.org.uk)**

## Usage

Installation instructions for Miranda can be found at http://miranda.org.uk/downloads/

```bash
mira -exec main.m part1 < file.txt
mira -exec main.m part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/13))

Our puzzle input defines the locations of a bunch of dots on a transparent sheet, and a few folds to perform on that sheet.
When we perform a fold, some of the dots will align and appear as only one dot.

**Part 1** has us perform the first fold and count the number of visible dots.
The answer for my input is 729.

**Part 2** has us perform the rest of the folds, and read the resultant drawn characters as the solution.
The answer for my input is RGZLBHFP.

## Retrospective

Ahh, back in SEO hell.

Miranda is a sort of proprietary proto-Haskell, and as I understand it it's been largely superseded by it.
No one really writes Miranda anymore.
You can really feel this trying to find information about it online.
I usually had more luck searching for how Haskell does something and just trying that, than trying to search how Miranda does it.

The saving grace here is Miranda ships with some pretty solid documentation built-in, including a bunch of examples of working programs (including one for drawing ascii art!).
And there are a few pockets of [very useful info](https://github.com/garrett-may/miranda-documentation/blob/master/standard_environment/standard_environment.md) available online.

Miranda thoughts:
- I found Miranda easier than the other functional languages this year, I think in part due to practice, but also because Miranda is a little less strict than the other languages. I was surprised that I didn't even have to enumerate all my patterns.
  - IO's way easier.
    There's just a var for stdin that you can read from as many times as you want.
    I bet this compromises pure-functional ideals somehow[^monad], but in this moment I'm not complaining!
- Unary stars for generic arguments is hellish.
  My eyes glass over looking at `(* -> ** -> *) -> * -> [**] -> *`.
  It's possible this is learned--letters as generic arguments don't mean much until you learn the notation.. but eesh.
- Significant whitespace that _requires tab characters_. Augh!
  Past this initial hurdle though the code flowed pretty smoothly.
  I had way fewer weirdo indentation errors than I did in Haskell!

Today's problem was all implementation/debugging, no tricky algorithm stuff, which I'm cool with.
I do enjoy the Advent of Code thing where solving the problem correctly writes big block letters to the screen.
Always a treat.

I think practically I'm not going to have much reason to return to Miranda, but I had a fun time with it!
Glad I'm getting a little more comfortable with the functional paradigm.

[^monad]: I think Miranda predates monads being used in functional programming
