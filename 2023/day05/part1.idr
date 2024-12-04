module Main

import Data.Bits
import Data.List
import Data.List1
import Data.SortedSet
import Data.String
import Aoc.Input
import Aoc.Result
import Aoc.Util

record Mapping where
  constructor MkMapping
  src, dest, width : Nat

Show Mapping where
  show this = "\{show this.src} \{show this.dest} \{show this.width}"

parseLine : String -> Maybe Mapping
parseLine line =
  case forget (map stringToNatOrZ (split (== ' ') line)) of
    (a::(b::(c::[]))) => Just (MkMapping a b c)
    _ => Nothing

main : IO ()
main = do
  lines <- readLines
  -- let seeds = map stringToNatOrZ (partition (== ' ') (head lines))
  let maybeSections = map tail' (tail (splitOn "" lines))
  case allOk (map (okOr "missing section") maybeSections) of
    Ok sections => do
      let sects = map (map parseLine) sections
      println sects
    Err err => println err
