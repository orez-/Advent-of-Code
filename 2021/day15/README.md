# Day 15: Chiton

**Language: [OCaml](https://ocaml.org/)**

## Usage

Installation instructions for OCaml can be found here https://ocaml.org/docs/install.html

```bash
ocaml part1.ml < file.txt
ocaml part2.ml < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/15))

The puzzle input gives us a grid of digits, and describes the cost of a path between two cells as the sum of the digits visited (excluding the first digit).

**Part 1** asks for the smallest cost between the top left cell and the bottom right cell.
The answer for my input is 366.

**Part 2** expands the grid.
We duplicate the grid five times in the x direction, raising the cost by 1 in each cell each time.
We also do the same in the y direction.
Where this would cause the cost to exceed 9, we loop around instead.

We're asked again to find the smallest cost between the top left and bottom right cells.
The answer for my input is 2829.

## Retrospective

Wasn't super enthusiastic about this puzzle, honestly.
We've done grid search already this year, and associating a (strictly positive) cost with it just meant I'd have to hunt down a priority queue in whatever language I ended up using.

Which brings me to OCaml.
A functional language with mutable types!
I enjoyed working with OCaml well enough, but I never totally figured out how it's meant to be invoked.
The [`Core`](https://opensource.janestreet.com/core/) module seemed like it had a bunch of very helpful utilities, but despite installing it I could never figure out how to link it to my execution.
In searching for an answer it was apparent this is a very common question, but I'm not completely satisfied with any of the answers I saw.
Seems like in larger projects you can define your includes in an `.ocamlinit` file, but if you're just running the `ocaml` interpreter it will _never_ respect the `.ocamlinit`, no matter what you do.
Which is fine, but I couldn't get this to work with `ocamlc`, `ocamlopt`, or `ocamlfind` either.
I don't fully understand what each of those do, or why there need to be three of them.
Most of the question threads I found ended with "aha, this works with the custom REPL. Problem solved!"
But I wasn't looking for a REPL, I was looking for a single command line command.
Overall it wasn't a great ramping-up experience.
As a result I had to find my own implementation of a priority queue to include in the file, my own hacky stdin-reader (which I truly butchered).
I don't think there's even an immutable hash map structure in Base OCaml, I ended up using a mutable one.

Once I had all these pieces together the solve wasn't so bad.
I remembered my idea from [day09](../day09) and stored the board state as spots to visit instead of seen spots to avoid, which totally bit me in part 2.
It would've been nice to keep just the initial grid and dynamically calculate the other 24, but that approach was incompatible with my implementation.
Other than that, pretty standard, pretty straightforward [best-first search](https://en.wikipedia.org/wiki/Best-first_search).
