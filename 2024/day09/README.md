# Day 9: Disk Fragmenter

## Usage

```bash
cargo run --bin day09 part1 < input.txt
cargo run --bin day09 part2 < input.txt
```

## Problem Summary ([?](https://adventofcode.com/2024/day/9))

The problem input describes the data on a disk, with files and free space of different sizes.
We're asked to defrag the disk.

We're also given a checksum algorithm to describe the disk state.
The checksum for each chunk is the index of the chunk multiplied by the file id at that chunk, and the checksum for the disk is the sum of the checksum of each chunk.

In **part 1** we can split files, and are asked to move the rightmost file chunks to the leftmost free spaces.
The answer for my input is 6386640365805.

In **part 2** we must keep the files contiguous, but are still asked to move the rightmost files to the leftmost free spaces which have enough space.
The answer for my input is 6423258376982.

## Retrospective

Heyy today kicked my ass a little!
Burned a lot of cycles waffling on what I wanted to optimize for in my design: code quality, runtime performance, ease of writing.
In part 1 I went for runtime performance, to nobody's benefit.
We iterate forward through the files, counting their contribution to the checksum, while simultaneously iterating backwards to move chunks into the forward gaps we encounter and counting THEIR contributions.
Notably we're not moving any files: we're only tracking the checksum.
This ought to be fast, and also way more trouble than it's worth: it was a pain to write, and I suspect it's a pain to read.

Decided to optimize for ease of writing in part 2, but still struggled a bit with the design here!
I started with an enum for `File(id)` and `Free` kept in a `Vec`, but splicing out files to move them and maintaining their surrounding gaps sounded just awful.
Ended up reworking this data structure to only track `File`s, and keeping them in a `BTreeMap` keyed by their start position.
This meant removing a file was dead simple, and though it complicated the gap-finding search a bit, linear searching through the ordered `BTreeMap` wasn't so bad.

I had also assumed that we'd be allowed to move a file to partially overlap with its current position, but the example indicates this isn't allowed.
Originally I was lifting the file before unconditionally placing it in the leftmost slot (since in the worst case we could drop it back where it started), but I had to change this to not lift, and ensure the slot we found was actually an improvement.

Good problem!
We're ramping up.
