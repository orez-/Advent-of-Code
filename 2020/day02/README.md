# Day 2: Password Philosophy

## Problem Summary ([?](https://adventofcode.com/2020/day/2))

We are given a list of lines, each containing a password string and a condition on that password's validity.
We are asked to count the number of valid passwords.

**Part 1** states that the two numbers in the condition represent a range.
The password string must contain a count of the given character within that range.
For instance, `1-3 a: abcde` is valid, because it contains one `a` and it must contain one to three.
With this ruleset 572 passwords in my input are valid.

**Part 2** states instead that the two numbers in the condition represent one-indexed indices into the password string.
A valid password has the given character at _exactly_ one of these positions (not both!).
With this ruleset 306 passwords in my input are valid.


## Retrospective

Straightforward early-day puzzle.
A couple reading comprehension gotchas, but I was able to parse the info quickly and correctly.
This has been a problem for me in past years, so I'm glad to be improving there.

Part 2 tripped me up a little because I adjusted the one-index the wrong direction.
Quick to debug, but this caused me to just miss placement.
I also spent too many cycles putting together an unnecessary index out-of-bounds check.
A small overoptimization, but I think it cost me a little.

I did manage to place top 50 on part 1 though! Can't complain about that.
