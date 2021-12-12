# Day 11: Dumbo Octopus

**Language: [Kotlin](https://kotlinlang.org/)**

## Usage

The installation instructions for Kotlin recommend you install IntelliJ IDEA and use the project wizard to start a new project, but that sentence makes my skin crawl.

Installation instructions for Kotlin can be found at https://kotlinlang.org/docs/command-line.html

```bash
kotlinc main.kt -include-runtime -d main.jar
java -jar main.jar part1 < file.txt
java -jar main.jar part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/11))

The problem input describes a 10 by 10 grid of dumbo octopuses.
Each digit in the input is the energy level of one octopus, between 0 and 9.
Each step the energy level of each octopus rises by 1, and once it passes 9 the octopus **flashes**.
When an octopus flashes all eight of its neighbors have their energy levels raised by 1 again, which may trigger further flashes.
All octopuses who flashed will reset to 0 energy after this process.

**Part 1** asks the total number of times octopuses flash in the first 100 steps.
The answer for my input is 1747.

After some number of steps all the octopuses start flashing in sync.
**Part 2** asks for the first time all octopuses flash at once.
The answer for my input is 505.

## Retrospective

I have to admit, I was really worried when I read the installation instructions.
A (text based) programming language that requires an IDE to operate is not anything I want to associate with.
Kotlin absolutely wants you to use their IDE, but fortunately it's not nearly as required as it first appears.

Past that bad first impression though, Kotlin is really nice!
The quickstart guide and docs are really strong, and it even has a page for [competitive programming](https://kotlinlang.org/docs/competitive-programming.html) which is fun and loosely relevant.
And the language has a bunch of nice modern design choices.
It's not quite able to smooth over all of Java's warts, but it's still pretty impressive.

- The Typescript-y type guard statements are a fun paradigm.
  I really like that all nulls in Kotlin are explicit, and that there's proper tooling to work with them.
- Using the [`sequence`](https://kotlinlang.org/docs/sequences.html#from-chunks) function with Kotlin's one-line function definition syntax is slick as hell.
  I like that this also makes it explicit which functions are generators, even if the function never actually `yield`s.
- Inclusive ranges bit me once, even after I checked that they were inclusive.
- Compile times were several seconds just for my small lil script.
  I imagine this is amortized for larger projects, but it wasn't my favorite.

My implementation for the puzzle wasn't anything special.
Every step we populate a queue of positions to increment, and when an octopus goes above 9 we add its neighbors to the queue as well.
Then we clear all the octos above 9.
