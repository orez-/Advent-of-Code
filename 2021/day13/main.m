loadCoords = map parseCoord (takewhile ("" ~=) (lines $-))
loadCreases = map parseCrease (tl (dropwhile ("" ~=) (lines $-)))

parseCoord :: [char] -> (num, num)
parseCoord line
      = parse' [] line
	where
	parse' sofar (a:line)
		= (numval sofar, numval line), if a = ','
		= parse' (sofar ++ [a]) line, otherwise

parseCrease :: [char] -> (char, num)
parseCrease ('f':'o':'l':'d':' ':'a':'l':'o':'n':'g':' ':c:'=':n)
      = (c, numval n)

|| "fold" as in the problem definition, not a functional fold
foldPt :: (char, num) -> (num, num) -> (num, num)
foldPt ('x', coord) (x, y)
	= (x, y), if x <= coord
	= (2 * coord - x, y), otherwise
foldPt ('y', coord) (x, y)
	= (x, y), if y <= coord
	= (x, 2 * coord - y), otherwise

foldPts :: (char, num) -> [(num, num)] -> [(num, num)]
foldPts crease pts
	= mkset (map (foldPt crease) pts)

foldedPaper = foldr foldPts loadCoords (reverse loadCreases)

draw :: (num, num) -> char
draw coord
	= '#', if (member foldedPaper coord)
	= ' ', otherwise

part1 = #(foldPts (hd loadCreases) loadCoords)

part2 :: [char]
part2 = concat [[draw (x, y) | x <- [0..40]] ++ "\n" | y <- [0..6]]

main = main' $*
	where
	main' (file:"part1":xs) = (show part1) ++ "\n"
	main' (file:"part2":xs) = part2
	main' args = "Please specify 'part1' or 'part2'\n"
