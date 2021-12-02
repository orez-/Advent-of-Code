# Day 19: Monster Messages

## Problem Summary ([?](https://adventofcode.com/2020/day/19))

The first half of the problem input describes a grammar for matching text.
Rules may take three different forms:
- `1: "a"` means rule 1 matches the character `a` literally.
- `0: 1 2` means rule 0 matches text that matches rule 1 followed by rule 2.
- `2: 1 3 | 3 1` means rule 2 may either match rule 1 then 3, or rule 3 then 1.

The second half of the problem input is a list of messages to match against.
We are tasked with determining the number of messages that completely match rule 0.

**Part 1** makes a point to mention that there are no loops in the puzzle input.
For my input 216 messages match these rules.

**Part 2** alters two of the rules:
```
8: 42 | 42 8
11: 42 31 | 42 11 31
```
The problem notes that this creates a loop.
For my input 400 messages match these rules.


## Retrospective

Fun puzzle!
I made a bunch of assumptions about the input and hardcoded a bunch of stuff, instead of trying to generalize.
I think it would've been less code to generalize, but not worth the overhead of getting it wrong and having to debug it.

For part 1 I parsed out all the rules into a dict of the form:
```python
{
    "1": "a",
    "0": [["1", "2"]],
    "2": [["1", "3"], ["3", "1"]],
}
```
Then I created a `matches` function to match a rule against a string.
If the rule was a literal prefix match I returned the string without that prefix.
Otherwise I tried all the different options for the rule, and called `matches` recursively to pare off prefixes, returning the first option that matched.
If the rule didn't match I returned `None`, and I counted any prefix matches that came out as the empty string as full matches.

I had a suspicion this wasn't exactly right, but I thought I might be able to get away with it since there were no loops.
I _did_ get away with it (and placed pretty well in the process), but this wasn't necessarily correct.
Consider the following input:
```
0: 1 | 2
1: "aaa"
2: "aaaaa"

aaaaa
```
My solution would see that `1` matched and return that, but then fail the full match check.
I'm lucky I didn't run into this; I hope the input was designed such that no one did!

For comparison, my solution to part 2 _is_ generalized enough to handle this case (see [`cleanup.py`](cleanup.py)).
Instead of returning the first result I `yield` all remaining suffixes after a match.
A string full-matches if it ever yields the empty string.
This allows us to explore the entire possibility space, instead of just taking the first prefix match.
I have a little experience with this pattern of `yield`ing possible matches from a [toy regex engine](https://github.com/orez-/RegHex/blob/master/regish.py) I put together as part of another project a few years ago, which definitely helped me here.
All the same, I had trouble keeping straight the possibilities;
what I was operating on and what the `matches` function was actually looking to return.
I ended up trying to hardcode a special case for the new rules, which helped me understand the problem better and eventually get the solution, but it didn't account for the `matches` API change correctly.
The last thing I did before getting the solution working was delete that block.
Feels like a bad use of time to write a bunch of unnecessary code, but it did get me there.
Placed in the 80s for this part.
I haven't been placing the past couple days, so I can't complain about whatever points I can pick up!
