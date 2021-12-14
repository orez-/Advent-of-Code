# Day 14: Extended Polymerization

**Language: [Nim](https://nim-lang.org/)**

## Usage

Installation instructions for Nim can be found at https://nim-lang.org/install.html

```bash
nim c -r --verbosity:0 part1.nim < file.txt
nim c -r --verbosity:0 part2.nim < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/14))

The problem input defines an initial string ("polymer"), and a series of transformations to apply, of the form `AC -> B`
For each step, we match every two character substring from our polymer with a rule (`AC`), and add `B` to the middle.
The resulting string becomes our new polymer.
We'll repeat this process several times.
In the end, we're asked to find the count of the most common character and the least common character in the polymer, and subtract the latter from the former.

**Part 1** asks us to run 10 steps.
The answer for my input is 3095.

**Part 2** asks us to run 40 steps.
The answer for my input is 3152788426516.

## Retrospective

Today's problem is a good one: the naive solution will work for part 1, but for part 2 the polymer simply balloons in size too quickly.
The trick to making it work is very similar to the trick from [day 6](../day06): rather than maintaining the whole string, we can just maintain counts of pairs.
There's a little bit of post-processing necessary at the end, since we've got character pairs but need individual characters.
But if we note that (almost!) each character in our pairs is counted twice, we can simply halve our totals to find the counts.
The only thing to watch out for are the two characters which are NOT counted twice: the first and last character.

Nim seems very Python-inspired, but isn't afraid to try new things, so I have a lot of thoughts about it!

- The big obvious similarity to Python is the significant whitespace.
  Largely, writing Nim felt like writing Python but with good static typing instead of Python's frustrating type annotation system.
  I dig it.
- I first learned about Nim from its [zany identifier equality rules](https://nim-lang.org/docs/manual.html#lexical-analysis-identifier-equality).
  I don't love this!
  I don't think making your code grep-resilient is a good idea.
- Nim brought back Dylan's `block` statement!
  I do really like `block` as semantically explicit syntax to mark an arbitrary region as "`break`able".
- Nim [moves the bitwise operators into names](https://nim-lang.org/docs/tut1.html#basic-types-integers) instead of symbols.
  I like this direction, although it's a little footgun-y if you were hoping `3 and 5` worked like Python.
  - Also the `&` operator still exists as.. prepend??
    It's Haskell's `:` operator!
    Wild.
  - And `^` is used for from-right list access!
    I had this idea like a year or two ago!
    Because Python's negative numbers as from-right list access is great for constants but a foot gun for variables!
    I even had the idea to repurpose a bitwise operator for it, though I had imagined the only traditionally-unary operator, `~`.
    I think I like `^` better though.
    Good on ya, Nim!
  - [`distinct` types](https://nim-by-example.github.io/types/distinct/) is really smart.
    Rust kind of achieves something similar with its [thin wrapper types](https://doc.rust-lang.org/rust-by-example/generics/new_types.html), but having the explicit `distinct` keyword makes the intention really clear.
  - Nim makes a handful of decisions in the name of C compatibility, and for all the ones I saw I believe the language would be improved without them.
    Ordinal enums, null-terminated strings.
    I guess if you want C compatibility they're nice, but Nim makes so many cool design decisions, I would've liked to see a version of the language that made even more cool decisions.
  - Anything returned has to be used or `discard`ed.
    This rules, I love this.
  - Inclusive ranges, wild.
    Bitten again.

Overall, I like it!
