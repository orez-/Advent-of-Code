module Main

import Data.Fin
import Data.List
import Data.Maybe
import Data.Nat
import Data.SortedMap
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

isGear : Board -> (Integer, Integer) -> Bool
isGear board coord = isJust (isGear' board coord) where
  isGear' : Board -> (Integer, Integer) -> Maybe ()
  isGear' board (y, x) = do
    yFin <- integerToFin y (length board)
    let row = unpack (index' board yFin)
    xFin <- integerToFin x (length row)
    let chr = index' row xFin
    if chr == '*'
      then Just ()
      else Nothing

partGears : Board -> PartNo -> List (Integer, Integer)
partGears board word = do
  let y = cast word.y
  let left = (cast word.x) - 1
  let right = cast (word.x + word.width)
  let topRow = map (MkPair (y - 1)) [left..right]
  let bottomRow = map (MkPair (y + 1)) [left..right]
  let edges = [(y, left), (y, right)]
  filter (isGear board) (concat [topRow, bottomRow, edges])

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

data GearNo = One Nat | Two Nat | Many
two : GearNo -> Maybe Nat
two (Two x) = Just x
two _ = Nothing

Show GearNo where
  show (One x) = "One " ++ (show x)
  show (Two x) = "Two " ++ (show x)
  show Many = "Many"

step : Maybe GearNo -> Nat -> GearNo
step Nothing num = One num
step (Just (One num1)) num2 = Two (num1 * num2)
step _ _ = Many

populateMap : (Nat, k) -> SortedMap k GearNo -> SortedMap k GearNo
populateMap (val, key) smap =
  let newVal = step (lookup key smap) val in
  insert key newVal smap

main : IO ()
main = do
  board <- readLines
  let words = concat (mapWithIndex findPartNos board)
  let gears = concat (map (\word => map (MkPair word.number) (partGears board word)) words)
  let gearMap = foldr populateMap empty gears
  let gearNums = catMaybes (map two (values gearMap))
  let sum = foldr (+) 0 gearNums
  putStrLn (show sum)
