module Aoc.Input

export
readLines : IO (List String)
readLines = do
  line <- getLine
  if line == "" then pure [] else do
    moreInputs <- readLines
    pure (line :: moreInputs)
