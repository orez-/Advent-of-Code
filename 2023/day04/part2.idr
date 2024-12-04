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

runCounts : (Nat, Nat) -> Maybe (List Nat) -> Maybe (List Nat)
runCounts _ Nothing = Nothing
runCounts (idx, wins) (Just counts) =
  let by = index idx counts {ok=believe_me Refl} in
  case idx + wins < (length counts) of
    true => Just (foldr (\at, list => increment by at list {ok=believe_me Refl}) counts [idx+1..idx+wins])
    false => Nothing

main : IO ()
main = do
  lines <- readLines
  let scores = map cardScore lines
  let eScores = mapWithIndex MkPair scores
  -- [1] * (length lines)
  let cardCounts = replicate (length lines) 1
  case (foldr runCounts (Just cardCounts) eScores) of
    Just answer =>
      let sum = foldr (+) 0 cardCounts in
      println sum
    Nothing => println "oob error"
