module Main

import Data.List
import Data.Nat
import Data.SortedSet

readLines : IO (List String)
readLines = do
  line <- getLine
  if line == "" then pure [] else do
    moreInputs <- readLines
    pure (line :: moreInputs)

lineToRow : String -> List Int
lineToRow row = map (\c => (ord c) - (ord '0')) (unpack row)

-- Idris2 reclaimed the name `index'` to enforce length via `Fin`.
-- This is the definition from Idris1.
-- https://github.com/idris-lang/Idris-dev/blob/d30e505cfabfce97bdfdd940464f74fe14100c22/libs/prelude/Prelude/List.idr#L112-L118
index' : (n : Nat) -> (l : List a) -> Maybe a
index' Z     (x::xs) = Just x
index' (S n) (x::xs) = index' n xs
index' _     []      = Nothing

inBounds : List (List Int) -> (Nat, Nat) -> Bool
inBounds board (x, y) =
  case (index' y board) of
  Just row => case (index' x row) of
    Just elem => elem /= 9
    Nothing => False
  Nothing => False

dfsArea : List (List Int) -> (Nat, Nat) -> SortedSet (Nat, Nat) -> (SortedSet (Nat, Nat), Int)
dfsArea board (x, y) seen = if contains (x, y) seen || not (inBounds board (x, y))
  then (seen, 0)
  else let seen' = insert (x, y) seen in
    let (seen1, area1) = dfsArea board (pred x, y) seen' in
    let (seen2, area2) = dfsArea board (x, pred y) seen1 in
    let (seen3, area3) = dfsArea board (S x, y) seen2 in
    let (seen4, area4) = dfsArea board (x, S y) seen3 in
    let area = area1 + area2 + area3 + area4 + 1 in
    (seen4, area)

dfsAreaAgg : List (List Int) -> (SortedSet (Nat, Nat), List Int) -> (Nat, Nat) -> (SortedSet (Nat, Nat), List Int)
dfsAreaAgg board (seen, areas) spot =
  let (seen', area) = dfsArea board spot seen in
  (seen', (area :: areas))

main : IO ()
main = do
  lines <- readLines
  let heights = map lineToRow lines
  let allSpots = [ (x, y) | y <- [0..(length heights)], x <- [0..100] ]
  let (_, areas) = foldl (dfsAreaAgg heights) (empty, []) allSpots
  let areas' = take 3 (reverse (sort areas))
  let product = foldl (*) 1 areas'
  putStrLn (show product)
