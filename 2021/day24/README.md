# Day 24: Arithmetic Logic Unit

**Language: [Yoix](https://github.com/att/yoix)**

## Usage

Installation instructions for Yoix can be found at https://github.com/att/yoix

Replace `$YOIX_HOME` below as appropriate.

```bash
alias yoix='java -jar "$YOIX_HOME/yoix.jar"'
yoix main.yx part1 < file.txt
yoix main.yx part2 < file.txt
```

## Problem Summary ([?](https://adventofcode.com/2021/day/24))

This problem describes a small instruction set for an arithmetic language.
With four registers `w`, `x`, `y`, and `z` (all initially 0), we apply the instructions from our input as follows:

- `inp a` reads an input value and writes it to register `a`.
- `add a b` adds the value of `a` to `b` and stores the result in `a`.
- `mul a b` multiplies the value of `a` to `b` and stores the result in `a`.
- `div a b` divides `a` by `b` and stores the result in `a`, truncating any fractional part.
- `mod a b` takes the remainder of `a / b` and stores the rseult in `a`.
- `eql a b` stores `1` in `a` if `a` equals `b`, otherwise stores `0`.

`b` may be a register or an integer.
`a` will always be a register.

`inp a` will read a digit (1-9) from the "input", which is a 14 digit number.

We're told an input is considered "accepted" if after computation we're left with 0 in the `z` register.

**Part 1** asks what the largest accepted number is.
The answer for my input is 59998426997979.

**Part 2** asks what the smallest accepted number is.
The answer for my input is 13621111481315.

## Retrospective

Loved this problem.
We obviously don't want to check all 10<sup>14</sup> options, so we have to find a way to simplify the input.
I ended up applying a bunch of checks, but from a high level I track the maximum and minimum value a term can have.
Knowing that an input digit `a` is [1, 9] means `a + 13` is in the range [14, 22], eg.
This also means `a + 13` does not equal `b`, since `b` can only get as high as 9.

This doesn't quite get us the answer though: I was only able to simplify the input to, like, a page and a half of equation.
In addition to this, I started tracking non-resolvable `eql` statements as both `0` and `1`, and seeing how each of these possibilities evolve.
In the end only one of these possibilities can be zero (and happens to necessarily be zero), which leaves us with the conditionals we assumed.
And it turns out those conditionals are all of the form `a + constant = b`, giving us the upper and lower bounds for those pairs.

I'm not sure if there was another way to approach this.
There might have been a trick with trying to find patterns in the input file by hand instead.
This solve took me a few sittings.
It was a lot of fun to do, but I'm not even sure what corners I would've cut for a fast solve.
I started out prototyping a solution in Python, but when it became clear this was pretty involved I ended up doing the whole solve in Python!
Kind of lame, but I did still transcribe my code to the language for today.

As far as the language, we're getting to some tough letters to find languages for.
I only found 3 "Y" languages, and since I wasn't going to do this in x86 assembly I went with Yoix, AT&T's proprietary take on JavaScript by way of Java.

Yoix's docs state that it doesn't have user-created classes, but DOES offer \~140 of your favorite Java classes, though I'll mention none of **my** favorites were there.
In particular, something ArrayList-ish would have been very nice.
The Yoix Array class can't grow[^array], which makes it tricky to work with if you happen to need exactly that.
I ended up writing my own Vec "typedef", "typedef" seemingly being a synonym for class?
Just with some bulky syntax surrounding it.
I'm sure I'm wielding typedef inelegantly here, but it got the job done.

Actually, a little something was lost in translation from Python to Yoix: it turns out my solution makes use of numbers larger than 32 bits, which overflowed in Yoix.
This doesn't affect the correct configuration, but means we get weird results for the other configurations.
Whatever!
I'm over it.

I'm sure Yoix has or had its niche, but as a general programming language I'm not enamored.
Props to it for starting with the letter Y, but I'm pretty comfortable not revisiting this one.

[^array]: I think? I couldn't find it in the docs at least. Please let me know if I'm wrong!
