# Day 6: Lanternfish

**Language: [Futhark](https://futhark-lang.org/)**

## Usage

Bear with me now.

Installation instructions for Futhark can be found at https://futhark.readthedocs.io/en/stable/installation.html .
Futhark is a pure functional language for working with numbers, so it doesn't really do IO.
We can't and shouldn't be trying to run it directly.
Instead we'll compile our Futhark code into a Python library, and use a small Python script to transform the input into a format Futhark can use.
Installation instructions for Python can be found at https://www.python.org/downloads/ .

```bash
python3 -m pip install numpy  # we're also going to need numpy
futhark python aoc.fut --library
```

```bash
python3 main.py part1 < file.txt
python3 main.py part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/6))

This puzzle describes the reproductive rates of lanternfish:
- Once mature, a lanternfish will give birth to another lanternfish every **7** days.
- Once born, a lanternfish takes **2** days to mature.

We're given a list of integers between 0 and 6.
Each integer represents a lanternfish, and the number of days before it will give birth.

**Part 1** asks us how many lanternfish there will be after 80 days.
The answer for my input is 355386.

**Part 2** asks us how many lanternfish there will be after 256 days.
The answer for my input is 1613415325809.

## Retrospective

Full disclosure, I ended up writing the solution for this one in Python first.
It looked like a fun one for Python (and it was!).
You can see this solution in [`original.py`](original.py).
The algorithm is basically the same.

```bash
python3 original.py part1 < file.txt
python3 original.py part2 < file.txt
```

---

I don't want to make a habit in this Advent of Code adventure of pre-handling inputs with a language I'm more familiar with, but in this case this is truly the intended pattern for Futhark.
It's intended to be used as a fast, pure functional drop-in library to crunch numbers.
I spent some time seeing if there was a way to get Futhark to read the input as bytes, but the more I looked into the clearer it became that this isn't how it's meant to be used.

I had never heard of Futhark before yesterday!
I found it mentioned in a rando's twitter bio.
It looked very cool (and to jump ahead a bit, it totally is), but the docs made it very explicit that Futhark is built for a particular purpose.
It is _not_ intended as a general-purpose language.
I was a bit worried that today's problem would not be a good fit for Futhark.
Something string heavy or data-structure-heavy probably would've been a no-go.

Even for the puzzle we got, I barely scratched the surface of what makes Futhark so powerful.
The sales pitch for Futhark is that many of the list operation primatives can leverage the GPU to achieve fast parallelization.
This makes it great for applying successive operations over a ton of data; not so much for applying an operation to the same small array iteratively.
Still, once I got a handle on the functional flow I really enjoyed working with Futhark.
The syntax is expressive and the documentation is strong, with plenty of examples.
I don't know if I'll ever get an opportunity to work with Futhark in a more appropriate context, but I hope that I will.

In terms of the problem, simulating each lanternfish individually seemed like a too-slow solution.
Instead we keep an array of seven elements, where each element is the count of lanternfish who will give birth that day of the week.
This means we can just iterate through the days, and each iteration we'll know exactly how many more lanternfish there will be.
We need to be a little careful not to just dump new fish back into the breeding pool though.
In order to model the two days to maturity we add their count to a queue of two elements.
We only add the fish to the breeding pool once they're forced off the queue.
