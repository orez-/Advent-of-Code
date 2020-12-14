# Day 14: Docking Data

## Problem Summary ([?](https://adventofcode.com/2020/day/14))

The puzzle input contains instructions of a programming language with only two commands.
The `mask` command sets the global mask value to some 36-bit value, where some of the bits can be `X`.
The `mem` command sets a memory address to some value, but it is modified by the mask somehow.

In **part 1** the mask applies to the value we're setting.
Mask bits of `1` or `0` get overwritten on this value.
`X`s are unchanged.
We're tasked with finding the sum of the values in memory after the program runs.
The answer for my input is 17481577045893.

In **part 2** the mask applies to the memory address.
Mask bits of `1` or `0` are bitwise-or'd into the address, but `X` values represent _both_ `1` and `0`.
We set the value for all memory addresses that match the address, with `X`s as wildcards.
We're still tasked with finding the sum of the values in memory after the program runs.
The answer for my input is 4160009892257.


## Retrospective

My first step with this puzzle was to find-replace the input into a simple space-separated format, because FORGET trying to parse that original format under time pressure.

For part 1 I converted the mask into a dictionary mapping the bit to its value.
Then when assigning mem values I just iterated the dictionary and set the bits manually.
If I were writing this code professionally I'd probably make it a list of tuples instead of a dictionary, since I only ever iterate over it, but I wasn't totally sure for the quick solve.
In fact the thought crossed my mind that I could just keep two values: the bits to set and the bits to remove, but that felt like an easy to mess up and hard to debug solution.

Although, I ended up doing something similar to that in part 2 anyway.
The `1` and `0` bits comprise a value to bitwise-or into the memory address, and I kept a value to remove for the `X` bits.
I also kept a set of the bits individually so I could powerset all the options back into the value to assign into memory.

And that was it!
I didn't place for part 1, but I made within top 50 for part 2.
Not bad.

My internet went out RIGHT after I successfully submitted part 2.
Phew!
