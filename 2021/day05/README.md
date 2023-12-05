# Day 5: Hydrothermal Venture

**Language: [Emojicode](https://www.emojicode.org/)**

## Usage

Installation instructions can be found at https://www.emojicode.org/docs/guides/install.html

```bash
emojicodec main.🍇
./main part1 < file.txt
./main part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/5))

The problem input contains a list of 2d line segments.
We're tasked with finding the count of (integer) coordinates where at least two line segments overlap.
Note that some of these line segments are colinear.

**Part 1** has us look at only the line segments that are horizontal or vertical.
The answer for my input is 8622.

**Part 2** has us look at all the line segments, though notes all line slopes are divisible by 45°.
The answer for my input is 22037.

## Retrospective

Of the languages I've used so far this year, somehow Emojicode is the one I have the most previous experience with.
But I haven't really played with it since 2016, and the language has changed a lot since then.
They reworked the meaning of a lot of the symbols to be less arbitrary (`🔢` probably makes more sense for numbers than `🚂` did).
And they've dropped the prefix notation.
I kind of miss the prefix notation!
It was charming, if not entirely practical.

In fact a lot of modern Emojicode is surprisingly practical.
- Mutability was a concern when I used Emojicode last, but back then there were two separate emoji for declaring a mutable variable `🍮` vs declaring an immutable variable `🍦`.
  Now immutable is the default, and you need [extra symbols](https://www.emojicode.org/docs/reference/variables.html#declaring-and-assigning-mutable-variables) to declare (`🖍🆕`) and assign to (`🖍`) mutable variables, reinforcing the idea that immutability should be your default.
  I like it!
- Object fields are always instance-private, which is enforced by syntax.
  You can access instance fields unqualified when in scope, and call methods on an instance `🔝foo` but there's no way to express `foo.top` or anything like that.
- The standard library is lightweight but contains most of the basics.
  It's got error handling, an optional type `🍬`, protocols, and even generics (eat your heart out, Go).
- The documentation is comprehensive, clear, and searchable.
  I do wish the class documentation had more usage examples instead of just type definitions, but the syntax is consistent enough that it's not a huge issue.
- Emojicode even uses Yarn for [package management](https://www.emojicode.org/docs/guides/yarn.html)!
  This is wild to me.
  I love it.

I floundered a bit on the actual solve.
For my initial pass at the problem I tried calculating the overlaps carefully, but it got gnarly really quickly.
Realized I needed to scrap that and just enumerate all the positions on the lines, and track those.
This also made part 2 much easier.
It's good to know I'm still overthinking Advent of Code, even without the time pressure.
Puzzle troubles aside though, I really enjoyed working with Emojicode again.
At this point it definitely feels like a fully featured language, which happens to use emoji heavily for syntax.

Some final Emojicode thoughts:
- Emojicode doesn't have a Set class, but there is a [Dictionary class `🍯`](https://www.emojicode.org/docs/packages/s/1f36f.html).
  Unfortunately its dictionary keys are always strings.
  It took me a while to figure out why the dict generic only wanted one type.
  I hope a Hashable interface (`#️⃣`? `🥔`?) is on the horizon soon.
- [Method moods](https://www.emojicode.org/docs/reference/classes-valuetypes.html#methods) are a fun idea.
  Encodes a little semantic meaning into what's effectively the closing paren of a function call.
  I like it.
- It's really a shame that `👉` is a reserved operator in emojicode.
  I unironically think `👉` and `👆` might be better names for horizontal and vertical offset than `x` and `y` in any language.
