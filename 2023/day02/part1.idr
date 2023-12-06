module Main

import Data.List
import Data.List1
import Data.String
import Data.String.Extra
import Aoc.Input
import Aoc.Result

partition : (Char -> Bool) -> String -> (String, String)
partition pred str =
  let (a, b) = break pred str in
  (a, drop 1 b)

record Round where
  constructor MkRound
  red, green, blue : Nat

Show Round where
  show this = "{red: " ++ (show this.red) ++ ", green: " ++ (show this.green) ++ ", blue: " ++ (show this.blue) ++ "}"

-- ugh
lte : Round -> Round -> Bool
lte x y = x.red <= y.red && x.green <= y.green && x.blue <= y.blue

newRound : Round
newRound = MkRound 0 0 0

max : Round -> Round -> Round
max a b = MkRound (max a.red b.red) (max a.green b.green) (max a.blue b.blue)

||| "4 red" -> Ok (MkRound 4 0 0)
parseColor : String -> Result Round String
parseColor line =
  let (countStr, color) = partition (== ' ') (trim line) in
  case parsePositive {a=Nat} countStr of
    Just count => case color of
      "red"   => Ok (MkRound count 0 0)
      "green" => Ok (MkRound 0 count 0)
      "blue"  => Ok (MkRound 0 0 count)
      _ => Err ("Unexpected color: '" ++ color ++ "'")
    Nothing => Err "Could not parse count"

||| "4 red, 18 green, 15 blue" -> Ok (MkRound 4 18 15)
readRound : String -> Result Round String
readRound line =
  let colorCounts = split (== ',') line in
  case allOk (forget (map parseColor colorCounts)) of
    Ok list => Ok (foldr max newRound list)
    Err err => Err err

readGame : String -> Result (Nat, Round) String
readGame line =
  let (header, roundsStr) = partition (== ':') line in
  case partition (== ' ') header of
    ("Game", rest) =>
      case parsePositive rest of
        Just gameNum =>
          let roundsRes = map readRound (split (== ';') roundsStr) in
          case allOk (forget roundsRes) of
            Ok rounds => Ok (gameNum, foldr max newRound rounds)
            Err err => Err err
        Nothing => Err "Could not parse game number"
    _ => Err "Could not parse game header"

main : IO ()
main = do
  lines <- readLines
  case (allOk (map readGame lines)) of
    Ok list => do
      let possible = filter ((`lte` (MkRound 12 13 14)) . snd) list
      let answer = foldr ((+) . fst) 0 possible
      putStrLn (show answer)
    Err e => putStrLn e
