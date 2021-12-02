# Day 4: Passport Processing

## Problem Summary ([?](https://adventofcode.com/2020/day/4))

The input file defines a bunch of passports, separated by blank lines.
A passport is a three-letter key, followed by a colon, followed by a value, and separated by some whitespace.
We are tasked with counting "valid" passports.

**Part 1** defines a valid passport as one that has all of the following fields:
`byr`, `iyr`, `eyr`, `hgt`, `hcl`, `ecl`, and `pid`.
The answer for my input is 170.

**Part 2** defines validation rules for each of the required fields:
- byr (Birth Year) - four digits; at least 1920 and at most 2002.
- iyr (Issue Year) - four digits; at least 2010 and at most 2020.
- eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
- hgt (Height) - a number followed by either cm or in:
  - If cm, the number must be at least 150 and at most 193.
  - If in, the number must be at least 59 and at most 76.
- hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
- ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
- pid (Passport ID) - a nine-digit number, including leading zeroes.

The answer for my input is 103.


## Retrospective

An implementation challenge.
For part 1 I lost some time because my record-splitting code didn't return the last record, and I ended up counting _all_ the records instead of just the valid ones due to a bug.
Looking at it now, instead of writing a generator to collect lines I should've just rejoined as a big string and split on `\n\n`.
Lost a bunch of time here.

For part 2 I lost some time trying to extract the value from the string of the key instead of the whole thing.
Silly mistake.

Implementing all the individual checks went pretty smoothly though.
Went for a cheeky `return '1920' <= v <= '2002'` check for the in-range fields.
I had a suspicion I could get away with this, and I did, but I could've just as easily gotten tripped up by something like `192[`.
I'm still happy with this decision.

Didn't place!
Next time.
