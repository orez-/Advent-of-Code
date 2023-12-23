module Main

import Data.Bits
import Data.List
import Data.List1
import Data.SortedSet
import Data.String
import Aoc.Input
import Aoc.Util

-- how does this not exist???
length : SortedSet _ -> Nat
length sset = length (Data.SortedSet.toList sset)

parseNumbers : String -> SortedSet Nat
parseNumbers line =
  let chunks = forget (split (== ' ') line) in
  let numStrs = filter (/= "") chunks in
  let nums = map stringToNatOrZ numStrs in
  fromList nums

cardScore : String -> Integer
cardScore line =
  let (_, line) = partition (== ':') line in
  let (winningNums, myNums) = partition (== '|') line in
  let winners = intersection (parseNumbers winningNums) (parseNumbers myNums) in
  case length winners of
    0 => 0
    len => shiftL 1 (pred len)

main : IO ()
main = do
  lines <- readLines
  let scores = map cardScore lines
  let sum = foldr (+) 0 scores
  println sum
