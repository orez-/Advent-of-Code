# Day 4: Giant Squid

**Language: [Dylan](https://en.wikipedia.org/wiki/Dylan_(programming_language))**

## Usage

Installation instructions can be found at https://opendylan.org/download/index.html

```bash
dylan-compiler -build day04/day04.lid
_build/bin/day04 part1 < file.txt
_build/bin/day04 part2 < file.txt
```

The initial build is surprisingly lengthy.

## Problem Summary ([?](https://adventofcode.com/2021/day/4))

The puzzle definition provides 100 bingo boards, the numbers that will be called against them, and the rule for how to score them once a bingo is achieved (ignoring diagonals).
The score of a completed bingo board is the sum of its uncalled values times the last number called against it.

**Part 1** asks the score of the **winning** bingo board, ie the board that reaches bingo first.
The answer for my input is 50008.

**Part 2** asks the score of the **losing** bingo board, ie the board that reaches bingo last.
The answer for my input is 17408.

## Retrospective

Dylan is the first language this year I hadn't really heard of at all.
Having now used it, I'm sorry to say this is probably for good reason.

Things I liked:
- Dylan has a built-in multidimensional array type!
  I went for this instead of a flat vector for the bingo boards to try to make the most of the lang.
  In practice it didn't seem to provide much functionality at all outside of what a flat vector would have given me... but still!
- Dylan classes don't have methods.
  The language instead prefers to have module-level functions that act on classes.
  This _rules_.
  This is what all dynamic languages should be doing.
  It's such an annoyance in Python to see a method on a class that you would have liked to reuse for some other type (often, notably, a mock).
  Many things might want to quack![^python]
- Once I found the pieces of the more functional programming side of Dylan, I really enjoyed using them.
  `reduce(\+, 0, choose(identity, board.cells))`?
  `any?(curry(call-number, num), boards)`?
  Heck yes, more like this please.
- Having control flow only interruptable with a callback from a `block` command is a neat idea.
  Makes explicit when some code may exit prematurely.
  I'm not sure how helpful I would actually find this, but it's an interesting approach.
- Dylan's [multiple dispatch](https://opendylan.org/documentation/intro-dylan/multiple-dispatch.html) seems very neat, but there wasn't a good opportunity in this challenge to try designing anything that would leverage it.

Things I didn't like:
- Error messages are pretty bad as compared to modern languages.
  The optional static typing is a nice idea, but the (runtime) error message `50008 is not of type {<class>: <boolean>}` isn't helpful without a line number.
  Like, yeah! Agreed! Sure isn't that type!

  In another instance I spent a lot of time trying to understand the error message:
  ```dylan
  let foo = 17 / 5;
  ```

  ```
  No applicable method, applying {<incremental-generic-function>: /} to {<simple-object-vector>: 17, 5}.
  ```
  I _think_ that `<simple-object-vector>` just refers to a plain old object, but the docs [really seem to indicate](https://opendylan.org/documentation/cheatsheet.html) that division like this should be legal.
  In the end I found the `truncate/` function, which is probably a more correct version of what I wanted anyway.
- Messing up the syntax of a statement within a for-loop just _skips the entire dang loop_ at runtime.
  One time I missed a semicolon closing an if-block in my read loop, and suddenly the entire loop was elided.
  In Dylan's defense, it did emit a "Serious warning" at compile time that it was doing this, but it decided to nestle this above the warning that I wasn't using my object's implicit setter function and I missed it.
- At one point I passed a named parameter to a function that did not accept a parameter with that name, and the program just hung.
  ```dylan
  define function main
      (name :: <string>, arguments :: <vector>)
    // !! Note that the correct argument is `remove-if-empty?`, with the trailing `?`
    split("Hello world", " ", remove-if-empty: #t);
    exit-application(0);
  end function main;
  ```
  I still don't know why that would be, but it wasn't a great experience.
- The name "Dylan" turns out to work against it in terms of SEO.
  More than once I'd search a question about something in Dylan to only receive results about someone named Dylan asking my question about javascript.
  Unhelpful!
  This combo'd really painfully with:
- The documentation feels pretty lacking in detail.
  I still don't know if there's a good way to populate an array.
  I think even just a few examples of usage would've gone a long way here.
  As it stands I probably got more insight from browsing the [Open Dylan](https://github.com/dylan-lang/opendylan) codebase than I got from the documentation.
- Dylan uses `x = y` to test equality, `x == y` to test identity, and `x := y` as assignment.
  This is totally fine, but then it uses a macro(?) `let x = 5;` as declaration and assigment.
  I'm sure there's a valid mindset where this makes sense but the seeming inconsistency strikes a beginner like me as footgun-ish.
- Whatever syntax highlighting I was using balked at named arguments, which made it tough to tell at a glance if I messed up or if I had just used a named argument.
  This isn't a strike against Dylan, but I still didn't like this!

It took me a really long time to get part 1 together.
Lots of scrounging for syntax and built-ins, and lots of debugging when I inevitably used them wrong.
Once I had the basics for part 1 done though, part 2 came together fairly quickly.

I came out of yesterday's challenge feeling like I hadn't really done justice to COBOL.
I'm sure what I've got today isn't perfect, but I definitely put more of a conscious effort into trying to understand how Dylan is intended to be used, and I think I did an alright job.
I don't think I'll be returning to Dylan anytime soon, but it's got some neat ideas that I'm glad to have explored.

[^python]: Technically Python (3+) does let you use `Foo.method(bar)` with a `bar` unrelated to `Foo`, but semantically this kind of sucks!
