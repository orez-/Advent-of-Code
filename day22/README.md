# Day 22: Slam Shuffle

## Problem Summary ([?](https://adventofcode.com/2019/day/22))

This problem describes the steps for a "shuffling algorithm", composed of three different types of actions:

- `cut n` rotates the deck by `n`. `n` may be positive or negative.
- `deal with increment n` redistributes the deck by dealing a card every `n` spots, for `|deck|` spots.
  We loop back over when we hit the end.
- `deal into new stack` reverses the deck.

The problem input contains many of these commands in sequence.
A deck of cards contains cards numbered `0` to `|deck|-1`, and starts sorted.

**Part 1** asks us to apply the shuffling algorithm on a deck of size 10007, and to get the position of card 2019.
The answer for my input is 6638.

**Part 2** acts on a deck of size 119,315,717,514,047, and asks us the card at position 2020 after shuffling it 101,741,582,076,661 times.
The answer for my input is 77863024474406.


## Retrospective

Messed up part 1 because I read "what card is in position 2019" instead of "what is the position of card 2019".
Reread the entire problem twice before I noticed this.
In part 2 I assumed it was asking for the same thing: "position of card 2020", and finished implementing a first-pass solution for that before I realized it wanted "position 2020".
Enitrely my fault, and very, very frustrating!

For part 2 I recognized we'd need to work backwards: start at final position 2020, figure out the position of that card after undoing all the operations, and repeating that several trillion times.
Figuring out the undo operations was a huge pain in the ass.
In particular, I needed to solve the equation `new_pos = (num * old_pos) % num_cards` in terms of `old_pos` for the `deal with increment n` operation.
One of these days I need to sit down and really learn modular math.
I've run up against this kind of thing before and bounced off of it.
This time I spent maybe twenty minutes trying to find the term that ended up being "[modular inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse)".

This let me undo the list of instructions pretty quickly, but certainly not quick enough to do it a hundred trillion times.
The problem mentioned Halley's Comet, so I figured I'd probably be able to run a few million iterations before we started cycling.
No dice.
Put a bunch of optimizations into it, but no cycles in any timely fashion.

In the end I didn't end up solving this one!
Had to look up the answer, and was deeply unsatisfied with what the answer ended up being.
Seems that after working backwards, we were meant to identify that since each of the undo functions were modular-linear, they compose to a modular-linear function, ie `f(x) = ax + b mod d`.
We can find that, then solve for f<sup>101,741,582,076,661</sup>(2020) which is its own challenge.

In addition to learning about the modular inverse, today I learned that Python 3.8 introduces a built-in modular inverse via `pow(a, -1, b)`.
Cool.

I would've personally much rather this problem had not been included in Advent of Code.
I recognize that a lot of folks like problems like this, but this is not in the slightest the kind of problem I want to solve.
I felt very helpless on this one, and I'm not sure how I could've thought about it differently, or even how I could've known what to look up to learn more about it.
Glad I learned about modular inverse at least.
