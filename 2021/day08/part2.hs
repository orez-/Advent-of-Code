import Data.List ((\\), elemIndex, intersect, sort)
import Data.Maybe (fromJust)
import System.IO (isEOF)

-- abcefg  => 0 [6]
-- cf      => 1 [2]
-- acdeg   => 2 [5]
-- acdfg   => 3 [5]
-- bcdf    => 4 [4]
-- abdfg   => 5 [5]
-- abdefg  => 6 [6]
-- acf     => 7 [3]
-- abcdefg => 8 [7]
-- abcdfg  => 9 [6]

subset a b = intersect a b == a
normalize numLine = map sort $ split (==' ') numLine
ofSize xs size = filter (\x -> size == length x) xs

-- https://stackoverflow.com/a/4981265/1163020
split     :: (Char -> Bool) -> String -> [String]
split p s =  case dropWhile p s of
                      "" -> []
                      s' -> w : split p s''
                            where (w, s'') = break p s'

calculateEncodings codes = do
  -- 1 4 7 8 are unambiguous
  let one = head $ ofSize codes 2
  let four = head $ ofSize codes 4
  let seven = head $ ofSize codes 3
  let eight = head $ ofSize codes 7
  -- 3 is the only [5] that fully overlaps 1
  let three = head $ filter (subset one) $ ofSize codes 5
  -- 6 is the only [6] that does not fully overlap 1
  let six = head $ filter (not . subset one) $ ofSize codes 6
  -- 2 has the top-right line segment, 5 does not
  let top = ("abcdefg" \\ six) !! 0
  let five = head $ filter (not . elem top) $ ofSize codes 5
  let two = head $ filter (\x -> not (x `elem` [three, five])) $ ofSize codes 5
  -- 3 fully overlaps 9 but not 0
  let nine = head $ filter (three `subset`) $ ofSize codes 6
  let zero = head $ filter (\x -> not (x `elem` [six, nine])) $ ofSize codes 6
  [zero, one, two, three, four, five, six, seven, eight, nine]

decodeDigit encoding x = fromJust (elemIndex x encoding)

decodedValue line = do
  let components = split (=='|') line
  let numbers = normalize $ components !! 0
  let values = normalize $ components !! 1
  let encoding = calculateEncodings numbers
  let digits = map (decodeDigit encoding) values
  foldl1 (\x y -> 10*x+y) digits

readLines :: IO [String]
readLines = do done <- isEOF
               if done
                 then return []
                 else do value <- getLine
                         moreInputs <- readLines
                         return (value : moreInputs)

main = do lines <- readLines
          print . sum $ map decodedValue lines
