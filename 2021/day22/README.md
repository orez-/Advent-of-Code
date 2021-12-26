# Day 22: Reactor Reboot

**Language: [Virgil](https://github.com/titzer/virgil)**

## Usage

Installation instructions for Virgil can be found at https://github.com/titzer/virgil/blob/master/doc/wiki/GettingStarted.md .
It's just cloning the repo and putting its `bin` on your PATH.

Virgil doesn't have a standard library, so you need to link what they've got yourself.
Make sure the `$VIRGIL_HOME` environment variable is set.

```bash
virgil main.v3 $VIRGIL_HOME/lib/util/*.v3 -- part1 < file.txt
virgil main.v3 $VIRGIL_HOME/lib/util/*.v3 -- part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/22))

This problem deals with a 3D grid of cube-lights which are either on or off.
We flip on or off large, axis-aligned rectangular prisms of cubes at a time, as given by the puzzle input.
We're tasked with finding how many lights are on at the end.

In **part 1** we only apply transformations within the area -50 to 50 around the origin in all directions.
The answer for my input is 644257.

In **part 2** we apply all transformations.
The answer for my input is 1235484513229032.

## Retrospective

Good problem.
It's clear the naive solution of tracking and flipping each light individually won't be feasible for the full input, so we have to come up with something else.
It's not quite as easy as just summing the prism volumes: if two "on" prisms overlap we don't want that overlap to count twice.
Instead we introduce each prism to the scene one at a time, and when we overlap an existing prism we cut it into pieces without that overlap.
The geometry here is a little tricky, but I didn't end up having any issues with this.

Instead I had all my issues with Virgil.
My goodness!
It appears that Virgil is developed and maintained by two developers, and in a lot of ways it feels like it.
All the documentation is kept in loose markdown files in the repo.
Information is well-documented, but finding it is another story.
It took me a long time to find the page that it turned out was named "Getting Started" to even start running the compiler.
Longer than that to find how to pull in other files in your script[^how].

It seems like Virgil does not have a standard library, although it does provide a folder of helpful utilities in the repo.
I think I saw that you're supposed to copy whatever you need and no more.
Instead of that I just imported everything from that folder.
Even with those utilities I ended up having to write my own versions of some extremely basic functionality.

Virgil reminds me a lot of a looser Rust, or what I imagine C++ to look like (I have not done much C++).
It's got some neat ideas though!

- The functional stuff I dabbled with came together smoothly.
  The partial application syntax was very nice.
- And the ADT structural typing stuff seems neat.
  I didn't really get a chance to play around with it, but I wish I had.
  I haven't worked with a structural typing system I loved, but I'd love to find one I do.
- Strong compile-time error messages and error formatting, very reminiscent of Rust.
  Runtime errors less so, also reminiscent of Rust, although I find Rust's safety guarantees mean it tends to produce way fewer runtime errors.

Random gripes:

- Virgil decided to keep `null`??
  They've got structural typing, it feels like they could've avoided this.
- No pattern matching on strings.
  I kind of get it, but I don't love it.

Overall Virgil is a little rough, a little "batteries not included, and also instructions not included, and also toy not included".
But for a project put together by just two people, it's surprisingly polished, with some neat ideas executed well.
As the language exists today I don't have a lot of desire to keep working with it, but I'm rooting for it.
I hope to see the language continue to grow and evolve.

[^how]: You need to pass them as additional command line arguments.
