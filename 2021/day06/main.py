import sys
from numpy import array, int64
from aoc import aoc

fn = getattr(aoc(), sys.argv[1])
input_stream = map(int64, sys.stdin.read().split(','))
input_file = array(list(input_stream))
result = fn(input_file)
print(result)
