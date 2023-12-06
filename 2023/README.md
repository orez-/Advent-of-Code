# Advent of Code 2023

My solutions for [Advent of Code 2023](http://adventofcode.com/2023).

## Running Idris code

Installation instructions for Idris can be found at https://www.idris-lang.org/pages/download.html .
I found it easiest to just `brew install idris2`.

The `idris2` CLI command seems to require a bunch of flags, and some of them seem to not actually work (eg `IDRIS2_PATH`).
The easiest way to run these solutions is from this 2023 root directory using the [`run.sh`](./run.sh) script:

```bash
./run.sh day01 part1
```
