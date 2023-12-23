module Aoc.Util

import Data.List
import Data.String
import Data.String.Extra

export
mapWithIndex : (Nat -> a -> b) -> List a -> List b
mapWithIndex f xs = mapWithIndex' 0 xs
 where
  mapWithIndex' : Nat -> List a -> List b
  mapWithIndex' n [] = []
  mapWithIndex' n (x :: xs) = f n x :: mapWithIndex' (S n) xs

export
partition : (Char -> Bool) -> String -> (String, String)
partition pred str =
  let (a, b) = break pred str in
  (a, drop 1 b)

-- taken from Idris 0.6
export
replaceAt : (idx : Nat) -> a -> (xs : List a) -> {auto 0 ok : InBounds idx xs} -> List a
replaceAt Z y (_ :: xs) {ok=InFirst} = y :: xs
replaceAt (S k) y (x :: xs) {ok=InLater _} = x :: replaceAt k y xs
