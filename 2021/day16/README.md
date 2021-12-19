Holy moly!
I've spent almost all of my free time for the past three days working on this!
I'll write some words here tomorrow!

cat file.txt | tr -d '\n' | ./piet -v part1.gif
cat file.txt | tr -d '\n' | ./piet -v part2.gif

955
158135423448

Part 1 takes like a full minute to run, because of the way the interpreter has to re-explore the 4096 constant every time.
