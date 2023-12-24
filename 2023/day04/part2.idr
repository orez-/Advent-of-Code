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

cardScore : String -> Nat
cardScore line =
  let (_, line) = partition (== ':') line in
  let (winningNums, myNums) = partition (== '|') line in
  let winners = intersection (parseNumbers winningNums) (parseNumbers myNums) in
  length winners

increment : Nat -> (n : Nat) -> (xs : List Nat) -> {auto 0 ok : InBounds n xs} -> List Nat
increment by at counts =
  let val = index at counts in
  replaceAt at (val + by) counts

runCounts : (Nat, Nat) -> List Nat -> List Nat
runCounts (idx, wins) counts =
  let by = index idx counts in
  foldr (increment by) counts [idx+1..idx+wins]

main : IO ()
main = do
  lines <- readLines
  let scores = map cardScore lines
  let eScores = mapWithIndex MkPair scores
  -- let cardCounts = map (\_ => 1) lines
  let cardCounts = replicate (length lines) 1
  let cardCounts = foldr runCounts cardCounts eScores
  let sum = foldr (+) 0 cardCounts
  println sum
