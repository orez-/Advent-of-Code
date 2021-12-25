# Day 21: Dirac Dice

**Language: [Unicon](http://www.unicon.org/)**

## Usage

Installation instructions for Unicon can be found at http://www.unicon.org/

```bash
unicon -s part1.icn && ./part1
unicon -s part2.icn && ./part2
```

## Problem Summary ([?](https://adventofcode.com/2021/day/21))

The problem today describes a [two-player game](https://en.wikipedia.org/wiki/Zero-player_game) where players track pawns on a circular track labeled 1 to 10.
Players take turns rolling three dice and moving their total, gaining the number of points landed on.
The first player to reach the target score wins.

**Part 1** starts us with a deterministic d100: the die will roll a 1, then a 2, and so on until it reaches 100 and loops back to 1.
We're asked to calculate how many times the die will get rolled before any player reaches 1000 points.
The answer for my input is 598416.

**Part 2** replaces our deterministic d100 with a normal d3, and lowers the score to win to 21.
We're asked to calculate the outcome of all possible games, and count up which player wins each.
Our solution is the number of games won by the player who wins the most.
The answer for my input is 27674034218179.

## Retrospective

Wow!
I wasn't sure what to expect from Unicon.
It was more of a language to fill a letter than one I was actively looking forward to.
I hadn't realized Unicon (and Icon) were such influential languages, while still having some very neat quirks and idioms to learn.

Unicon (not "Unicorn" 🦄) is a dialect of Icon, which has better support for object oriented programming and I/O.
The two are otherwise pretty dang similar, to the point where a lot of help online lumps them together.

Unicon thoughts:
- I had heard Python was largely inspired by Smalltalk, but I'm seeing the Icon influences really apparently.
  - Co-expressions in particular, with the `suspend` keyword acting like a supercharged version of Python's `yield`.
  - Python even adopted Icon's list slice syntax `my_list[start:end]`.
    This is the only other language I've seen use this syntax: most languages I've seen this year use some form of `start..end` or `start to end`.
- Fallible expressions are a slick idea.
  There are no booleans; instead any expression may **succeed** and return a value, or **fail** and (I think) bubble up like an exception until caught.
  This means integer comparisons `x < y` are free to return extra information, and they opt to return the right operand.
  The consequence of this is we get operator chaining `x < y < z` for free, no special casing!
- We're back in nightmare SEO territory, but between the [book](http://www.unicon.org/book/ub.pdf), Rosetta code, and surprisingly decent error messages I didn't have too much trouble.

I think there's a lot more depth to Unicon than I explored, especially around the generator stuff.
Unicon's absolutely going on the list of languages to follow up on after this.

I was worried today was going to be a the yearly modulo problem, which always trip me up.
The straightforward approach was good enough for both parts though, with the help of a little memoization in part 2.
