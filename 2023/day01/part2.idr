module Main

import Data.Fin
import Data.List
import Data.Maybe
import Data.String
import Aoc.Input
import Aoc.Result

findNumb : (List Char) -> (List (List Char)) -> Maybe Integer
findNumb line nums =
  case findIndex (\c => isPrefixOf c line) nums of
    Just x => Just (finToInteger x)
    Nothing => case line of
      [] => Nothing
      (c::cs) => do
        let d = (ord c) - (ord '0')
        if d <= 9
          then Just (cast d)
          else findNumb cs nums

findNum : String -> Result Integer String
findNum line =
  let nums = map unpack ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"] in
  let tens = findNumb (unpack line) nums in
  let ones = findNumb (reverse (unpack line)) (map reverse nums) in
  case (tens, ones) of
    (Just a, Just b) => Ok (a * 10 + b)
    _ => Err "Could not parse number"

main : IO ()
main = do
  lines <- readLines
  case allOk (map findNum lines) of
    Ok list => do
      let result = sum list
      putStrLn (show result)
    Err err => putStrLn err
