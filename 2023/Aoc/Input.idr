module Aoc.Input

export
println : Show a => a -> IO ()
println x = putStrLn (show x)

export
readLines : IO (List String)
readLines = do
  line <- getLine
  if line == "" then pure [] else do
    moreInputs <- readLines
    pure (line :: moreInputs)
