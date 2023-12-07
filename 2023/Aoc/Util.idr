module Aoc.Util

export
mapWithIndex : (Nat -> a -> b) -> List a -> List b
mapWithIndex f xs = mapWithIndex' 0 xs
 where
  mapWithIndex' : Nat -> List a -> List b
  mapWithIndex' n [] = []
  mapWithIndex' n (x :: xs) = f n x :: mapWithIndex' (S n) xs
