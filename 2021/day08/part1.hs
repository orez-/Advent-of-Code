import System.IO (isEOF)

split     :: (Char -> Bool) -> String -> [String]
split p s =  case dropWhile p s of
                      "" -> []
                      s' -> w : split p s''
                            where (w, s'') = break p s'

-- Count the number of signals which could be a 1, 4, 7, or 8
count1478 line = do
    let output = split (=='|') line !! 1
    let nums = split (==' ') output
    length $ filter (`elem` [2, 3, 4, 7]) (map length nums)

readLines :: IO [String]
readLines = do done <- isEOF
               if done
                 then return []
                 else do value <- getLine
                         moreInputs <- readLines
                         return (value : moreInputs)

main = do lines <- readLines
          print . sum $ map count1478 lines
