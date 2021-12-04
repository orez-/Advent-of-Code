Module: day04
Synopsis: 
Author: 
Copyright: 

define constant $width = 5;
define constant $height = 5;

define class <board> (<object>)
  sealed slot cells :: <array>,
    required-init-keyword: cells:;
end;

define function read-board ()
  let output = read-line(*standard-input*, on-end-of-stream: #f);
  let cells = make(<array>, dimensions: #(5, 5));

  block(return)
    for (y from 0 below $height)
      let line = read-line(*standard-input*, on-end-of-stream: #f);

      if (~line)
        return(#f);
      end;
      let x = 0;
      for ( elem in split(line, " ", remove-if-empty?: #t) )

        cells[y,x] := string-to-integer(elem);
        x := x + 1;
      end;
    end;
    make(<board>, cells: cells);
  end block;
end function read-board;


// Call a number and return the score of the board if you've got Bingo.
// Otherwise return false.

define method call-number (num :: <number>, board :: <board>)
  let idx = find-key(board.cells, curry(\=, num));
  let output = #f;
  if (idx)
    board.cells[idx] := #f;
    // no methods to operate over rows / columns?
    // ...why am i using the 2d array class, then?
    let col = modulo(idx, $width);
    let row = truncate/(idx, $width);
    let full_row = every?(\~, map(method (y) board.cells[y, col] end, range(from: 0, to: 4)));
    let full_col = every?(\~, map(method (x) board.cells[row, x] end, range(from: 0, to: 4)));

    if (full_row | full_col)
      output := reduce(\+, 0, choose(method (x) x end, board.cells)) * num;
    end;
  end;
  output;
end method call-number;

define function main
    (name :: <string>, arguments :: <vector>)
  let nums = map(string-to-integer, split(read-line(*standard-input*), ","));
  let boards = make(<stretchy-vector>);
  let board = read-board();
  while (board)
    add!(boards, board);
    board := read-board();
  end;

  block(return)
    for (num in nums)
      let score = any?(curry(call-number, num), boards);
      if (score)
        format-out("%s\n", score);
        return();
      end;
    end;
  end block;
  exit-application(0);
end function main;

main(application-name(), application-arguments());
