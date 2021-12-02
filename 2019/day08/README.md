# Day 8: Space Image Format

## Problem Summary ([?](https://adventofcode.com/2019/day/8))

This problem defines an image format, where each charater in the input represents a pixel: 0 for black, 1 for white, and 2 for transparent.
The pixels are defined left to right, top to bottom, and then by layers frontmost to backmost.
The problem states that the given image is of text, and is 25 pixels wide by 6 pixels tall.

**Part 1** has you find the layer with the *fewest* 0s, and return its number of 1s times its number of 2s.
The answer for my input was 1088.

**Part 2** asks for the text displayed by the image.
This can be found by printing the pixels to the terminal and human-reading the result.
The answer for my input was LGYHB.

## Retrospective

Always, always, always reading comprehension.
I read so carefully, I didn't assume what the output was going to be, got it all down.
And then I found the layer with the **most** 0 digits instead of the fewest.
How frustrating.
I lost a full minute and probably 20 points total for that mistake.

Other than that everything went alright.
I lost a little time wrestling with the type of the elements I was grabbing from the file (str vs int), but nothing major.
Python's generators are as always a great way to iterate two differently shaped iterators without having to put a ton of thought into how to line up the zip, or whatever.
I didn't want to have to figure out how many complete layers there were, so I just kept eating the layer file and caught the StopIteration, which probably saved me a bunch of time.

This problem was similar to last year's [Day 10: The Stars Align](https://github.com/orez-/Advent-of-Code-2018/tree/master/day10) ([?](https://adventofcode.com/2018/day/10)) in how you're tasked with drawing image data to the terminal to read some text.
I can't imagine having done that problem gave me much of an edge, but still neat.
