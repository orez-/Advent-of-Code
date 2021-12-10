module Main

import Data.List

readLines : IO (List String)
readLines = do
  line <- getLine
  if line == "" then pure [] else do
    moreInputs <- readLines
    pure (line :: moreInputs)

window3_ : List a -> List (Maybe a, a, Maybe a)
window3_ Nil = []
window3_ (x::[]) = [(Nothing, x, Nothing)]
window3_ (x::y::[]) = [(Just x, y, Nothing)]
window3_ (x::y::z::xs) = (Just x, y, Just z) :: (window3_ (y::z::xs))

window3 : List a -> List (Maybe a, a, Maybe a)
window3 Nil = []
window3 (x::[]) = [(Nothing, x, Nothing)]
window3 (x::y::xs) = (Nothing, x, Just y) :: (window3_ (x::y::xs))

justify : Maybe (List (Maybe a, a, Maybe a)) -> List (Maybe a)
justify Nothing = List.replicate 100 Nothing
justify (Just list) = map (\(_, y, _) => Just y) list

-- You know this seemed like a good idea once.
surrFmt : (Maybe a, (Maybe a, a, Maybe a), Maybe a) -> (a, List a)
surrFmt (n, (w, c, e), s) = (c, catMaybes [n, e, w, s])

surrounding : List (List a) -> List (a, List a)
surrounding board =
  let windows = map (\(x, y, z) => (zip3 (justify x) y (justify z))) (window3 (map window3 board)) in
  map surrFmt (concat windows)

lineToRow : String -> List Int
lineToRow row = map (\c => (ord c) - (ord '0')) (unpack row)

main : IO ()
main = do
  lines <- readLines
  let heights = map lineToRow lines
  let surrs = surrounding heights
  let minima = filter (\(x, ys) => all (x <) ys) surrs
  let full = sum (map (\(height, _) => height + 1) minima)
  putStrLn (show full)
