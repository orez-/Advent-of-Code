# Day 3: Binary Diagnostic

**Language: [COBOL](https://en.wikipedia.org/wiki/COBOL)**

## Usage

```bash
sudo apt-get install open-cobol
```

```bash
cobc -free -x -o part1 part1.cob && ./part1 < file.txt
cobc -free -x -o part2 part2.cob && ./part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/3))

In **part 1** we're given a list of 12-bit integers, and tasked with constructing a composite of the most likely bits to be set (called "gamma").
That is, the first bit of our composite should be 1 if 1 is the most common first bit in the list, and so on for each bit.
We're also tasked with finding the composite of the _least_ common bits (called "epsilon"), and our solution is the product of these two values.
The answer for my input is 1092896.

**Part 2** transposes the operations from part 1 and runs them iteratively: we find the most common values for the first bit and discard those that don't match, then repeat for the second bit and so on until only one value remains.
We do the same for the least common values, and multiply the two resultant values together for our solution.
The answer for my input is 4672151.

## Retrospective

This is my first experience writing COBOL, and oofda.
I don't think I've previously used a language that predates C, and I'm realizing I've really come to take for granted some of the programming language standards C has set.

What felt like the longest part of this process was spent just trying to understand what section headers were required, and which were keywords and which were identifiers.
It wouldn't be right to say it was smooth sailing once I figured out how to read from stdin and how to loop, but that initial step was really rough.
In terms of COBOL itself, having the code try to read as English words is kind of endearing, though I'd say it has mixed efficacy.
`ADD 1 TO X` is kind of a slick incrementer, but doubling a value with `MULTIPLY 2 BY X` doesn't have the same clarity, in my opinion.
And I still don't understand what `PICTURE` for data definition is trying to convey.

For part 1, it's true to say that the most-common value is the negation of the least-common value, and I did use this fact in a way.
I couldn't find a built-in function or anything to convert a string of binary to a decimal number, so in writing the converter I had it write each bit exactly once, to either the gamma or epsilon value.

For part 2 we have to reuse the input list many times, which meant storing the list instead of streaming it.
I'm not sure if COBOL has a way to dynamically allocate space, but I just made a couple sized arrays (well, [a table](https://www.tutorialspoint.com/cobol/cobol_table_processing.htm)) the size of the input, 1000 elements.
To discard elements from the table I just replaced them with blank sentinel values; this meant as we whittle the table down we still iterate over all 1000 entries.
We also have to be a little careful finding the _minimum_ occurring bit in the set.
The maximum is always the one that has over half of the total, but if all the bits are the same there's only one to choose from, and the minimum is the same as the maximum.
I addressed this by handling the special case where 1-count equals 0 or equals the total.

For these puzzles I'm trying my best to learn and utilize the idioms of the languages I'm using.
I could probably hack most of these together with the smallest subset of the language possible, with code that could be written in any language.
But what I'm really interested in is understanding what makes these languages unique and what they have to offer.
This is a tall ask for a daily puzzle challenge, and I'm not convinced my COBOL code here is particularly idiomatic.
I'd be interested in hearing about any tips or tricks I could've taken better advantage of here!
My experience with this problem has not inspired me write my next project in COBOL or anything like that, but I'm definitely curious if COBOL's hiding any cool tricks that could've made this a smoother solve.

One interesting note to call out here: a lot of the help I found online came from posts on random help forums.
And I was kind of shocked to find so many hostile responses to what were clearly beginner questions.
Actively rude tones, a lot of "did you even read the documentation?"
I'm used to Stack Overflow's moderated and informative responses, or the Rust or Python communities, which both make explicit efforts to foster beginner-friendly environments.
I don't know exactly what the disconnect is here (and this is all anecdotal besides), but I definitely found it jarring.
