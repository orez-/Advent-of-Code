module Main

import Data.List
import Data.Maybe
import Result

readLines : IO (List String)
readLines = do
  line <- getLine
  if line == "" then pure [] else do
    moreInputs <- readLines
    pure (line :: moreInputs)

findNum : String -> Result Int String
findNum line =
  let stream = map unsafeParseChr (unpack line) in
  case ((find (<= 9) stream), (find (<= 9) (reverse stream))) of
    (Just a, Just b) => Ok (a * 10 + b)
    _ => Err "Could not parse number"
  where
    unsafeParseChr : Char -> Int
    unsafeParseChr c = (ord c) - (ord '0')

main : IO ()
main = do
  lines <- readLines
  case allOk (map findNum lines) of
    Ok list => do
      let result = sum list
      putStrLn (show result)
    Err err => putStrLn err
