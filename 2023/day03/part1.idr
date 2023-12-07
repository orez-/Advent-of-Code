module Main

import Data.Fin
import Data.List
import Data.Maybe
import Data.Nat
import Data.String
import Aoc.Input
import Aoc.Util

record PartNo where
  constructor MkPartNo
  number, x, y, width : Nat

Show PartNo where
  show this = "\{show this.number} @ [\{show this.x}, \{show this.y}] (\{show this.width})"

Board : Type
Board = List String

||| Get the symbol at the coordinate.
get : Board -> Integer -> Integer -> Maybe Char
get board y x = do
  yFin <- integerToFin y (length board)
  let row = unpack (index' board yFin)
  xFin <- integerToFin x (length row)
  let chr = index' row xFin
  if (isDigit chr) || chr == '.'
    then Nothing
    else Just chr

isPartNumber : Board -> PartNo -> Bool
isPartNumber board word = do
  let y = cast word.y
  let left = (cast word.x) - 1
  let right = cast (word.x + word.width)
  let topRow = map (get board (y - 1)) [left..right]
  let bottomRow = map (get board (y + 1)) [left..right]
  let edges = [get board y left, get board y right]
  any isJust (concat [topRow, bottomRow, edges])

findPartNos : Nat -> String -> List PartNo
findPartNos y line =
  let (_, _, partNos) = foldr parseNo ((length line), [], []) (unpack line) in
  partNos where
    parseNo : Char -> (Nat, List Char, List PartNo) -> (Nat, List Char, List PartNo)
    parseNo chr (x, num, partNos) =
      if isDigit chr
        then if x == 1
          then makeNum 0 (chr::num) partNos
          else (pred x, chr::num, partNos)
        else if (length num) == 0
          then (pred x, num, partNos)
          else makeNum x num partNos
      where
        makeNum : Nat -> List Char -> List PartNo -> (Nat, List Char, List PartNo)
        makeNum x num partNos = do
          let width = length num
          -- i don't understand why this fn exists..
          let val = stringToNatOrZ (pack num)
          let partNo = MkPartNo val x y width
          (pred x, [], partNo::partNos)

partNumbers : Board -> List Nat
partNumbers board = do
  let words = concat (mapWithIndex findPartNos board)
  let partNos = filter (isPartNumber board) words
  map (.number) partNos

main : IO ()
main = do
  board <- readLines
  let sum = foldr (+) 0 (partNumbers board)
  putStrLn (show sum)
