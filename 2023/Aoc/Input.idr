module Aoc.Input
import Data.List
import System.File

export
println : Show a => a -> IO ()
println x = putStrLn (show x)

export
readLines : IO (List String)
readLines = do
  lines <- readLines2
  case init' lines of
    Just list => pure list
    Nothing => pure []
  where
    readLines2 : IO (List String)
    readLines2 = do
      eof <- fEOF stdin
      if eof then pure [] else do
        line <- getLine
        moreInputs <- readLines2
        pure (line :: moreInputs)
